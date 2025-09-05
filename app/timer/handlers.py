from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from app.timer.service import TimerService
from app.dependency import get_timer_service, get_request_user_id, get_user_service
import time
import json
import redis

from app.users.user_profile.service import UserService
from worker.celery import run_pomodoro_timer_task


router = APIRouter(prefix='/timer', tags=['timer'])
redis_client: Redis = redis.Redis(host='cache', port=6379)


def get_initial_state():
    return {
        "is_running": False,
        "session_type": "work",
        "work_duration": 25 * 60,
        "break_duration": 5 * 60,
        "start_time": None,
        "time_left": 25 * 60,
    }


@router.get('/{task_id}')
async def get_task_by_id(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                         user_id: int = Depends(get_request_user_id)):
    task = await timer_service.get_task_by_id(task_id=task_id, user_id=user_id)
    return task


@router.get('/start/{task_id}')
async def start_task(task_id: int, user_service: Annotated[UserService, Depends(get_user_service)],
                     timer_service: TimerService = Depends(get_timer_service),
                     user_id: int = Depends(get_request_user_id)):
    settings = await user_service.get_settings_user(user_id=user_id)
    print(type(redis_client))
    state = json.loads(redis_client.get(str(task_id)) or '{}')
    if state.get("is_running"):
        raise HTTPException(status_code=400, detail="Таймер уже запущен")
    task = await timer_service.get_task_by_id(task_id=task_id, user_id=user_id)
    new_state = get_initial_state()
    new_state.update({
        "is_running": True,
        "pomodoro_count": task.pomodoro_count,
        "work_duration": settings.work_duration * 60,
        "break_duration": settings.short_break_duration * 60,
        "time_left": settings.work_duration * 60,
        "start_time": time.time(),
    })
    redis_client.set(str(task_id), json.dumps(new_state))
    print(">>> sending task to celery:", str(task_id), type(str(task_id)), type(run_pomodoro_timer_task))
    run_pomodoro_timer_task.delay(str(task_id))
    return {"message": "Таймер запущен.", "state": new_state}


@router.post("/pause/{task_id}")
async def pause_timer(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                      user_id: int = Depends(get_request_user_id)):
    """Ставит таймер на паузу."""
    state_json = redis_client.get(str(task_id))
    if not state_json:
        raise HTTPException(status_code=404, detail="Таймер не найден")

    state = json.loads(state_json)
    permission = await timer_service.check_permission(task_id=task_id, user_id=user_id)
    if permission:
        if state["start_time"] is not None:
            current_duration = state["work_duration"] if state["session_type"] == "work" else state["break_duration"]
            elapsed = time.time() - state["start_time"]
            state["time_left"] = max(0, int(current_duration - elapsed))
        state["is_running"] = False
        await timer_service.change_status_planned(task_id=task_id)
        redis_client.set(str(task_id), json.dumps(state))
        return {"message": "Таймер на паузе.", "state": state}
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав доступа к этой задаче')


@router.post("/reset/{task_id}")
async def reset_timer(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                      user_id: int = Depends(get_request_user_id)):
    """Снимает таймер с паузы"""
    state_json = redis_client.get(str(task_id))
    if not state_json:
        raise HTTPException(status_code=404, detail="Таймер не найден")
    permission = await timer_service.check_permission(task_id=task_id, user_id=user_id)
    if permission:
        state = json.loads(state_json)
        state["is_running"] = True
        if state['session_type'] == 'work':
            state['start_time'] = time.time() + state['time_left'] - state['work_duration']
        else:
            state['start_time'] = time.time() + state['time_left'] - state['break_duration']
        await timer_service.change_status_in_progress(task_id=task_id)
        redis_client.set(str(task_id), json.dumps(state))
        return {"message": "Таймер снят с паузы.", "state": state}
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав доступа к этой задаче')


@router.get("/status/{task_id}")
async def get_status(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                     user_id: int = Depends(get_request_user_id)):
    """Возвращает текущее состояние таймера из Redis."""
    state_json = redis_client.get(str(task_id))
    if not state_json:
        return HTTPException(status_code=404, detail="Таймер не найден")
    permission = await timer_service.check_permission(task_id=task_id, user_id=user_id)
    if permission:
        return json.loads(state_json)
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав доступа к этой задаче')


@router.post('/end/{task_id}')
async def end_task(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                   user_id: int = Depends(get_request_user_id)):
    state_json = redis_client.get(str(task_id))
    if not state_json:
        raise HTTPException(status_code=404, detail="Таймер не найден")
    permission = await timer_service.check_permission(task_id=task_id, user_id=user_id)
    if permission:
        state = json.loads(state_json)
        state['is_running'] = False
        state['pomodoro_count'] = 0
        state['time_left'] = 0
        await timer_service.change_status_completed(task_id=task_id)
        redis_client.set(str(task_id), json.dumps(state))
        redis_client.delete(str(task_id))

        return {"message": "Задача досрочно завершена"}
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав доступа к этой задаче')


@router.post('/skip/{task_id}')
async def skip_step(task_id: int, timer_service: TimerService = Depends(get_timer_service),
                    user_id: int = Depends(get_request_user_id)):
    state_json = redis_client.get(str(task_id))
    if not state_json:
        raise HTTPException(status_code=404, detail="Таймер не найден")
    permission = await timer_service.check_permission(task_id=task_id, user_id=user_id)
    if permission:
        state = json.loads(state_json)
        if state['session_type'] == "work":
            state['session_type'] = "break"
            state['time_left'] = state['break_duration']
            state['pomodoro_count'] -= 1
        else:
            state['session_type'] = "work"
            state['time_left'] = state['work_duration']

        state['start_time'] = time.time()

        if state['pomodoro_count'] <= 0:
            state['is_running'] = False
            state['time_left'] = 0

        redis_client.set(str(task_id), json.dumps(state))
        return {"message": "Вы перешли к следующей фазе", 'state': state}
    else:
        raise HTTPException(status_code=403, detail='У вас нет прав доступа к этой задаче')
