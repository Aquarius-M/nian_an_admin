<template>
    <div>
        <el-card class="!border-none" shadow="never">
            <el-page-header content="用户详情" @back="$router.back()" />
        </el-card>
        <el-card class="mt-4 !border-none" header="基本资料" shadow="never">
            <el-form ref="formRef" class="ls-form" :model="formData" label-width="120px">
                <el-form-item label="头像：">
                    <div>
                        <div>
                            <material-picker v-model="formData.avatar" :limit="1" />
                        </div>
                        <!-- <div class="form-tips">建议尺寸：100*100px，支持jpg，jpeg，png格式</div> -->
                    </div>
                    <!-- <el-button type="primary" >确定</el-button> -->
                    <el-button type="primary" link v-perms="['user:edit']" @click="handleEdit(formData.avatar, 'avatar')">
                        确认
                    </el-button>
                    <el-button class="ml-[10px]" link type="danger" @click="resetEdit('avatar')"
                        v-perms="['user:reset']">重置</el-button>
                </el-form-item>
                <el-form-item label="用户编号："> {{ formData.sn }} </el-form-item>
                <el-form-item label="账号：">
                    {{ formData.username }}
                    <el-button link type="danger" class="ml-[10px]" @click="resetEdit('password')"
                        v-perms="['user:reset']">重置密码</el-button>
                </el-form-item>
                <el-form-item label="用户昵称：">
                    {{ formData.nickname }}
                    <popover-input class="ml-[10px]" :limit="32" :value="formData.nickname"
                        @confirm="handleEdit($event, 'nickname')">
                        <el-button type="primary" link v-perms="['user:edit']">
                            <icon name="el-icon-EditPen" />
                            <!-- 编辑 -->
                        </el-button>
                    </popover-input>
                    <el-button class="ml-[10px]" link type="danger" @click="resetEdit('nickname')"
                        v-perms="['user:reset']">重置</el-button>
                </el-form-item>
                <el-form-item label="性别：">
                    {{ formData.sex }}
                    <popover-input class="ml-[10px]" type="select" :value="formData.sex" :options="[
                        {
                            label: '未知',
                            value: 0
                        },
                        {
                            label: '男',
                            value: 1
                        },
                        {
                            label: '女',
                            value: 2
                        }
                    ]" @confirm="handleEdit($event, 'sex')">
                        <el-button type="primary" link v-perms="['user:edit']">
                            <icon name="el-icon-EditPen" />
                        </el-button>
                    </popover-input>
                </el-form-item>
                <el-form-item label="真实姓名：">
                    {{ formData.realName || '-' }}
                    <popover-input class="ml-[10px]" :value="formData.realName" :limit="32"
                        @confirm="handleEdit($event, 'realName')">
                        <el-button type="primary" link v-perms="['user:edit']">
                            <icon name="el-icon-EditPen" />
                        </el-button>
                    </popover-input>
                </el-form-item>

                <el-form-item label="联系电话：">
                    {{ formData.mobile || '-' }}
                    <popover-input class="ml-[10px]" type="number" :value="formData.mobile"
                        @confirm="handleEdit($event, 'mobile')">
                        <el-button type="primary" link v-perms="['user:edit']">
                            <icon name="el-icon-EditPen" />
                        </el-button>
                    </popover-input>
                </el-form-item>

                <el-form-item label="个性签名">
                    {{ formData.motto || '-' }}
                    <popover-input class="ml-[10px]" :value="formData.motto" :limit="300"
                        @confirm="handleEdit($event, 'motto')" type="textarea" :show-limit="true">
                        <el-button type="primary" link v-perms="['user:edit']">
                            <icon name="el-icon-EditPen" />
                            <!-- 编辑 -->
                        </el-button>
                    </popover-input>
                    <el-button class="ml-[10px]" link type="danger" @click="resetEdit('motto')"
                        v-perms="['user:reset']">重置</el-button>
                </el-form-item>

                <el-form-item label="注册来源："> {{ formData.channel }} </el-form-item>
                <el-form-item label="注册时间："> {{ formData.createTime }} </el-form-item>
                <el-form-item label="最近登录："> {{ formData.lastLoginTime }} </el-form-item>
                <el-form-item label="状态：" min-width="100">
                    <el-switch :model-value="formData.isDisable" :active-value="0" :inactive-value="1"
                        v-perms="['user:detail:disable']" @change="($event) => changeStatus($event, formData.id)" />
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script lang="ts" setup name="consumerDetail">
import type { FormInstance } from 'element-plus'
import { getUserDetail, userEdit, userStatus } from '@/api/consumer'
import feedback from '@/utils/feedback'
import { isEmpty } from '@/utils/util'
import { getUserSetup, } from '@/api/setting/user'

const route = useRoute()
const formData = reactive({
    id: 0,
    sn: '',
    avatar: '',
    nickname: '',
    username: '',
    realName: '',
    sex: '',
    mobile: '',
    motto: '',
    channel: '',
    createTime: '',
    lastLoginIp: '',
    lastLoginTime: '',
    isDisable: 0,
})

const formRef = shallowRef<FormInstance>()

const getDetails = async () => {
    const data = await getUserDetail({
        id: route.query.id
    })
    Object.keys(formData).forEach((key) => {
        //@ts-ignore
        formData[key] = data[key]
    })
}

const handleEdit = async (value: string, field: string) => {
    if (field == "sex") {
        if (value == "未知") {
            value = '0'
        } else if (value == "男") {
            value = '1'
        } else if (value == "女") {
            value = '2'
        }
    }
    if (isEmpty(value)) return
    await userEdit({
        id: route.query.id,
        field,
        value
    })
    feedback.msgSuccess('编辑成功')
    getDetails()
}

const resetEdit = async (field: string) => {
    await feedback.confirm('确定要重置？')
    const data = await getUserSetup()
    let value = ""
    if (field == "avatar") {
        value = data["defaultAvatar"]
    } else if (field == "nickname") {
        value = 'u' + formData.sn
    }
    else if (field == "password") {
        value = 'a123456'
    }
    await userEdit({
        id: route.query.id,
        field,
        value
    })
    feedback.msgSuccess('重置成功')
    getDetails()
}

const changeStatus = async (active: any, id: number) => {
    try {
        await feedback.confirm(`确定${active ? '停用' : '开启'}当前用户？`)
        await userStatus({ id })
        feedback.msgSuccess('修改成功')
        getDetails()
    } catch (error) {
        getDetails()
    }
}

getDetails()
</script>
