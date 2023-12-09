import request from '@/utils/request'

// 用户列表
export function getUserList(params: any) {
    return request.get({ url: '/user/list', params })
}

// 新增用户
export function userAdd(params: any) {
    return request.post({ url: '/user/add', params })
}

// 删除用户
export function userDel(params: any) {
    return request.post({ url: '/user/del', params })
}

// 用户详情
export function getUserDetail(params: any) {
    return request.get({ url: '/user/detail', params })
}

// 用户编辑
export function userEdit(params: any) {
    return request.post({ url: '/user/edit', params })
}

// 用户禁用
export function userStatus(params: any) {
    return request.post({ url: '/user/disable', params })
}
