from fastapi import APIRouter, Depends

from like.admin.schemas.user import UserListIn, UserDetailIn, UserEditlIn, UserDisableIn, UserDelIn
from like.admin.service.user.user import IUserService, UserService, UserInfoOut, UserCreateIn
from like.http_base import unified_resp
from like.schema_base import PageInationResult
from like.dependencies.log import record_log

router = APIRouter(prefix='/user')


@router.get('/list', response_model=PageInationResult[UserInfoOut])
@unified_resp
async def user_list(list_in: UserListIn = Depends(),
                    user_service: IUserService = Depends(UserService.instance)):
    """
    用户列表
    :return:
    """
    return await user_service.list(list_in)


@router.get('/detail')
@unified_resp
async def user_detail(detail_in: UserDetailIn = Depends(),
                      user_service: IUserService = Depends(UserService.instance)) -> UserInfoOut:
    """
    用户详情
    :return:
    """
    return await user_service.detail(detail_in=detail_in)

@router.post('/edit')
@unified_resp
async def user_detail(edit_in: UserEditlIn,
                      user_service: IUserService = Depends(UserService.instance)) -> UserInfoOut:
    """
    用户修改
    :return:
    """
    return await user_service.edit(edit_in=edit_in)



@router.post('/add', dependencies=[Depends(record_log(title='用户新增'))])
@unified_resp
async def add(user_create_in: UserCreateIn,
                     user_service: IUserService = Depends(UserService.instance)):
    """新增"""
    return await user_service.add(user_create_in)


@router.post('/del', dependencies=[Depends(record_log(title='用户删除'))])
@unified_resp
async def user_del(user_del_in: UserDelIn,
                    auth_service: IUserService = Depends(UserService.instance)):
    """用户删除"""
    return await auth_service.delete(user_del_in)

@router.post('/disable', dependencies=[Depends(record_log(title='用户状态切换'))])
@unified_resp
async def user_disable(user_disable_in: UserDisableIn,
                        auth_service: IUserService = Depends(UserService.instance)):
    """用户状态切换"""
    return await auth_service.disable(user_disable_in.id)