import { defineStore } from 'pinia'
import { BaseApi } from '../assets/base_api'

const api = new BaseApi()

export const useStore = defineStore('store', {
    state: () => ({
        user: {
        },
        is_self: false
    }),
    actions: {
        async verify_login() {
            const res = await api.post('/verify/', {})
            if (res.status == 200) {
                await this.get_user_info()
            }
            else {
                this.$state.user = {}
            }
        },
        async get_user_info() {
            const res = await api.post('api/user/get_user_info', {})
            if (res.status == 200) {
                this.$state.user = res.result.data;
            }
            else {
                console.log(res)
            }
        },
        async get_user_info_by_id(id: string) {
            const res = await api.post('api/user/get_user_info_by_id', {
                target_id: id
            })
            if (res.status == 200) {
                return res.result
            }
            else {
                console.log(res)
            }
        },
        
    }
})