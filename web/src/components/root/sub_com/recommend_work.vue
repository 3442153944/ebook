<template>
  <div class="recommend_work">
    <div class="work_list">
        <div class="work_item" v-for="(item,index) in work_list" :key="index">
            <img :src="'http://localhost:8000/static/img/'+(item.cover||'default_cover.jpg')" alt="封面">
            <div class="work_info">
                <span>{{item.title}}</span>
                <span>{{item.username}}</span>
                <span>{{item.novel_type_name}}</span>
            </div>
        </div>
    </div>
  </div>
</template>


<script setup>
import { ref,computed, onMounted } from 'vue'
import { useStore } from '@/model/store';
import { useRouter } from 'vue-router';
import { BaseApi } from '@assets/base_api';

const api=new BaseApi();
const store = useStore();
const router = useRouter();

let work_list=ref([]);

//获取推荐作品列表
async function get_recommend_work(){
    let res=await api.post('api/get_info/get_recommend_novel',{
        
    });
    if(res.status==200){
        work_list.value=res.result.data
    }
    else{
        console.log(res)
    }
}
onMounted(async ()=>{
    await get_recommend_work();
})

</script>

<style scoped>
.recommend_work{
    margin-left: 10px;
    width: 100%;
}
.work_list{
    display: grid;
    grid-template-columns: repeat(4,1fr);
    grid-gap: 10px;
    flex-wrap: wrap;
}
.work_info{
    display: flex;
    flex-direction: column;
    gap:5px;
}
</style>