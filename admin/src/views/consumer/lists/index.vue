<template>
    <div>
        <el-card class="!border-none" shadow="never">
            <el-form ref="formRef" class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="用户信息">
                    <el-input class="w-[280px]" v-model="queryParams.keyword" placeholder="用户编号/昵称/手机号码" clearable
                        @keyup.enter="resetPage" />
                </el-form-item>
                <el-form-item label="注册时间">
                    <daterange-picker v-model:startTime="queryParams.startTime" v-model:endTime="queryParams.endTime" />
                </el-form-item>
                <el-form-item label="注册来源">
                    <el-select class="w-[280px]" v-model="queryParams.channel">
                        <el-option v-for="(item, key) in ClientMap" :key="key" :label="item" :value="key" />
                    </el-select>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select class="w-[280px]" v-model="queryParams.isDisable">
                        <el-option v-for="(item, key) in StatusMap" :key="key" :label="item" :value="key" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="resetPage">查询</el-button>
                    <el-button @click="resetParams">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
        <el-card class="!border-none mt-4" shadow="never">
            <el-button v-perms="['user:add']" type="primary" @click="handleAdd">
                <template #icon>
                    <icon name="el-icon-Plus" />
                </template>
                新增
            </el-button>
            <el-button v-perms="['user:del']" :disabled="!selectData.length" type="danger"
                @click="handleDelete(selectData)">
                <template #icon>
                    <icon name="el-icon-Delete" />
                </template>
                删除
            </el-button>
            <div class="mt-4">
                <el-table size="large" v-loading="pager.loading" :data="pager.lists"
                    @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" />
                    <el-table-column label="用户编号" prop="sn" min-width="120" />
                    <el-table-column label="头像" min-width="100">
                        <template #default="{ row }">
                            <el-avatar :src="getCurrentImage(row.avatar)" :size="50" />
                        </template>
                    </el-table-column>
                    <el-table-column label="昵称" prop="nickname" min-width="100" />
                    <el-table-column label="账号" prop="username" min-width="120" />
                    <el-table-column label="性别" prop="sex" min-width="100" />
                    <el-table-column label="注册来源" prop="channel" min-width="100" />
                    <el-table-column label="注册时间" prop="createTime" min-width="120" />
                    <el-table-column label="状态" min-width="100">
                        <template #default="{ row }">
                            <el-switch :model-value="row.isDisable" :active-value="0" :inactive-value="1"
                                v-perms="['user:disable']" @change="($event) => changeStatus($event, row.id)" />
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120" fixed="right">
                        <template #default="{ row }">
                            <el-button v-perms="['user:detail']" type="primary" link>
                                <router-link :to="{
                                    path: getRoutePath('user:detail'),
                                    query: {
                                        id: row.id
                                    }
                                }">
                                    详情
                                </router-link>
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="flex justify-end mt-4">
                <pagination v-model="pager" @change="getLists" />
            </div>
        </el-card>
        <edit-popup v-if="showEdit" ref="editRef" @success="getLists" @close="showEdit = false" />
    </div>
</template>
<script lang="ts" setup name="consumerLists">
import { usePaging } from '@/hooks/usePaging'
import { getRoutePath } from '@/router'
import { getUserList, userStatus, userDel } from '@/api/consumer'
import { ClientMap, StatusMap } from '@/enums/appEnums'
import EditPopup from './add.vue'
import feedback from '@/utils/feedback'
import { onActivated, onMounted } from 'vue'
import useAppStore from '@/stores/modules/app'

const { getCurrentImage } = useAppStore()
const editRef = shallowRef<InstanceType<typeof EditPopup>>()

const queryParams = reactive({
    keyword: '',
    channel: '',
    startTime: '',
    endTime: '',
    isDisable: '',
})

const showEdit = ref(false)
const { pager, getLists, resetPage, resetParams } = usePaging({
    fetchFun: getUserList,
    params: queryParams
})

const handleAdd = async () => {
    showEdit.value = true
    await nextTick()
    editRef.value?.open('add')
}

const selectData = ref<any[]>([])

const handleSelectionChange = (val: any[]) => {
    selectData.value = val.map(({ id }) => id)
}

const handleDelete = async (ids: any[]) => {
    await feedback.confirm('确定要删除？')
    await userDel({ ids })
    feedback.msgSuccess('删除成功')
    getLists()
}

const changeStatus = async (active: any, id: number) => {
    try {
        await feedback.confirm(`确定${active ? '停用' : '开启'}当前用户？`)
        await userStatus({ id })
        feedback.msgSuccess('修改成功')
        getLists()
    } catch (error) {
        getLists()
    }
}

onActivated(() => {
    getLists()
})

onMounted(() => {
    getLists()
})

// getLists()
</script>
