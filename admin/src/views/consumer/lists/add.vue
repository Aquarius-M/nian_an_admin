<template>
    <div class="edit-popup">
        <popup ref="popupRef" :title="popupTitle" :async="true" width="550px" @confirm="handleSubmit" @close="handleClose">
            <el-form ref="formRef" :model="formData" label-width="84px" :rules="formRules">

                <el-form-item label="头像">
                    <div>
                        <div>
                            <material-picker v-model="formData.avatar" :limit="1" />
                        </div>
                        <div class="form-tips">建议尺寸：100*100px，支持jpg，jpeg，png格式</div>
                    </div>
                </el-form-item>

                <el-form-item label="昵称" prop="nickname">
                    <el-input v-model="formData.nickname" placeholder="请输入昵称" clearable />
                </el-form-item>

                <el-form-item label="账号" prop="username">
                    <el-input v-model="formData.username" placeholder="请输入账号" clearable />
                </el-form-item>

                <el-form-item label="密码" prop="password">
                    <el-input v-model.trim="formData.password" show-password clearable placeholder="请输入密码" />
                </el-form-item>

                <el-form-item label="确认密码" prop="passwordConfirm">
                    <el-input v-model.trim="formData.passwordConfirm" show-password clearable placeholder="请输入确认密码" />
                </el-form-item>

                <el-form-item label="性别" prop="sex">
                    <el-select v-model="formData.sex" class="flex-1" clearable :value="formData.sex" placeholder="请选择性别"
                        @change="handleEdit">
                        <el-option v-for="(item, index) in sexOptions " :label="item.label" :value="item.index"
                            :key="index" />
                    </el-select>
                </el-form-item>

                <el-form-item label="手机号码：" prop="mobile">
                    <el-input v-model="formData.mobile" placeholder="请输入手机号" clearable />
                </el-form-item>

                <el-form-item label="真实姓名：" prop="realName">
                    <el-input v-model="formData.real_name" placeholder="请输入真实姓名" clearable />
                </el-form-item>
            </el-form>
        </popup>
    </div>
</template>
<script lang="ts" setup>
import type { FormInstance } from 'element-plus'
import Popup from '@/components/popup/index.vue'
import feedback from '@/utils/feedback'
import { getUserDetail, userAdd, userEdit } from '@/api/consumer'
import { getUserSetup, } from '@/api/setting/user'

const emit = defineEmits(['success', 'close'])
const formRef = shallowRef<FormInstance>()
const popupRef = shallowRef<InstanceType<typeof Popup>>()
const popupTitle = computed(() => {
    return '新增用户'
})

const sexOptions = [
    {
        label: '未知',
        index: 0
    },
    {
        label: '男',
        index: 1
    },
    {
        label: '女',
        index: 2
    }
]

const formData = reactive({
    id: '',
    username: '',
    nickname: '',
    avatar: '',
    password: '',
    passwordConfirm: '',
    mobile: '',
    real_name: '',
    channel: 7,
    sex: 0,
    is_disable: 0,
    motto: '',
})

// 获取用户设置数据
const getData = async () => {
    try {
        const data = await getUserSetup()
        formData["avatar"] = data["defaultAvatar"]
    } catch (error) {
        console.log('获取=>', error)
    }
}

const handleEdit = (value: number) => {
    formData.sex = value;
}

const passwordConfirmValidator = (rule: object, value: string, callback: any) => {
    if (formData.password) {
        if (!value) callback(new Error('请再次输入密码'))
        if (value !== formData.password) callback(new Error('两次输入密码不一致!'))
    }
    callback()
}
const formRules = reactive({
    username: [
        {
            required: true,
            message: '请输入账号',
            trigger: ['blur']
        }
    ],
    nickname: [
        {
            required: true,
            message: '请输入名称',
            trigger: ['blur']
        }
    ],
    password: [
        {
            required: true,
            message: '请输入密码',
            trigger: 'blur'
        }
    ] as any[],
    passwordConfirm: [
        {
            required: true,
            message: '请再次输入密码',
            trigger: 'blur'
        },
        {
            validator: passwordConfirmValidator,
            trigger: 'blur'
        }
    ] as any[]
})

const handleSubmit = async () => {
    console.log(formData)
    await formRef.value?.validate()
    await userAdd(formData)
    popupRef.value?.close()
    feedback.msgSuccess('操作成功')
    emit('success')
}

const open = (type = 'add') => {
    popupRef.value?.open()
}

const handleClose = () => {
    emit('close')
}

defineExpose({
    open,
})
getData()
</script>
