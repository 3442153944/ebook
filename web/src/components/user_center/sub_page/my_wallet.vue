<template>
  <div class="my_wallet">
    <h2>我的资产</h2>
    <div class="content">
      <div class="money">
        <div class="balance">
          <span>余额</span>
          <span>￥{{wallet.money}}</span>
        </div>
        <div class="recharge">
          <span>充值</span>
        </div>
      </div>
      <div class="transaction_record">
        <h2>交易记录</h2>
        <div class="menu_item">
          <span @click="change_index(0)" :class="{is_change:now_index==0}">交易记录</span>
          <span @click="change_index(1)" :class="{is_change:now_index==1}">充值记录</span>
        </div>
        <div class="filter">
          <span>查询消费记录</span>
          <section>
            <span>开始时间</span>
            <input type="date">
            <span>结束时间</span>
            <input type="date">
          </section>
        </div>
        <div class="record_title">
          <span>交易时间</span>
          <span>交易类型</span>
          <span>交易金额</span>
        </div>
        <div class="record_list">
          <div class="record_item" v-for="(item,index) in now_list" :key="index">
            <span>{{item.time}}</span>
            <span>{{item.type}}</span>
            <span>{{item.money}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref,onMounted } from 'vue'

let wallet=ref({
  money:0,
  transaction_record:[
    {
      time:'2025-3-14 18:15:13',
      type:'充值',
      money:100
    }
  ],
  recharge_record:[
    {
      time:'2025-3-14 18:15:13',
      type:'支付宝',
      money:100
    }
  ]
})
let now_index=ref(0)
let now_list=ref([

])

function change_index(index){
  now_index.value=index
  if(index==0){
    now_list.value=wallet.value.transaction_record
  }
  else{
    now_list.value=wallet.value.recharge_record
  }
}
onMounted(()=>{
  change_index(0)
})

</script>

<style scoped>
.my_wallet {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h2 {
  font-size: 1.8rem;
  color: #1a1a1a;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #409eff;
}

.content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 2rem;
}

/* 余额区域 */
.money {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, #409eff 0%, #3375e0 100%);
  border-radius: 8px;
  color: white;
  margin-bottom: 2rem;
}

.balance span:first-child {
  font-size: 1.2rem;
  opacity: 0.9;
}

.balance span:last-child {
  font-size: 2.5rem;
  font-weight: bold;
  letter-spacing: 2px;
}

.recharge span {
  display: inline-block;
  padding: 0.8rem 2rem;
  background: rgba(255,255,255,0.15);
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid rgba(255,255,255,0.3);
}

.recharge span:hover {
  background: rgba(255,255,255,0.25);
  transform: translateY(-2px);
}

/* 交易记录 */
.transaction_record {
  margin-top: 2rem;
}

.menu_item {
  display: inline-flex;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 4px;
  margin: 1rem 0;
}

.menu_item span {
  padding: 0.8rem 2rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s;
}

.menu_item span:hover {
  background: #eef0f3;
}

.menu_item span.active {
  background: white;
  color: #409eff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* 时间筛选 */
.filter {
  margin: 1.5rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

input[type="date"] {
  padding: 0.6rem;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  color: #606266;
}

/* 记录列表 */
.record_title {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding: 1rem;
  background: #fafafa;
  color: #909399;
  border-radius: 6px;
  margin: 1rem 0;
}

.record_list {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
}

.record_item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding: 1.2rem;
  transition: all 0.2s;
  border-bottom: 1px solid #f5f7fa;
}

.record_item:last-child {
  border-bottom: none;
}

.record_item:hover {
  background: #fafafa;
}

.record_item span:nth-child(3) {
  color: #67c23a;
  font-weight: 500;
}
.is_change{
  background-color: rgb(0,150,250);
  color: white;
  font-size: 18px;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .money {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .filter {
    flex-direction: column;
    align-items: flex-start;
  }

  .record_title,
  .record_item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .record_title {
    display: none;
  }

  .record_item {
    position: relative;
    padding: 1.2rem;
  }

  .record_item span::before {
    content: attr(data-label);
    display: inline-block;
    width: 80px;
    color: #909399;
    font-size: 0.9rem;
    margin-right: 1rem;
  }

  .record_item span:nth-child(1)::before { content: "时间："; }
  .record_item span:nth-child(2)::before { content: "类型："; }
  .record_item span:nth-child(3)::before { content: "金额："; }
}
</style>