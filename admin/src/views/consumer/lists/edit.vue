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
            </el-form>
        </popup>
    </div>
</template>
<script lang="ts" setup>
import type { FormInstance } from 'element-plus'
import Popup from '@/components/popup/index.vue'
import feedback from '@/utils/feedback'
import { getUserDetail, userAdd, userEdit } from '@/api/consumer'
const emit = defineEmits(['success', 'close'])
const formRef = shallowRef<FormInstance>()
const popupRef = shallowRef<InstanceType<typeof Popup>>()
const popupTitle = computed(() => {
    return '新增用户'
})

const formData = reactive({
    id: '',
    username: '',
    nickname: '',
    avatar: '',
    password: '',
    passwordConfirm: '',
    channel: 7,
})


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
</script>
