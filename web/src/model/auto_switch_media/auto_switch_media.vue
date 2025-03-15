<template>
    <div class="auto_switch_media">
        <div class="media_container">
            <!-- 媒体内容 -->
            <transition :name="transitionEffect" mode="out-in">
                <div class="media_item" :key="currentIndex">
                    <div v-if="currentMedia.type === 'img'">
                        <img :src=" 'http://localhost:8000/static/'+currentMedia.url" alt="media" class="media_img">
                    </div>
                    <div v-else>
                        <video :src="'http://localhost:8000/static/'+currentMedia.url"  autoplay="true" loop="true" muted="true" class="media_video"></video>
                    </div>
                </div>
            </transition>
            <!-- 指示器 -->
        <div class="indicators">
            <div v-for="(item, index) in media_list" :key="index" class="indicator"
                :class="{ active: currentIndex === index }" @click="switchMedia(index)">
                <img src="./assets/中国结.svg" alt="中国结" class="icon">
            </div>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import {useStore} from '@/model/store';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();


const props = defineProps({
    media_list: {
        type: Array,
        default: () => [
            '春节.jpg',
            '过年.jpg',
            '过年2.jpg',
            '惊蛰.png',
            'm63895da90bb55.mp4'
        ]
    },
    interval: {
        type: Number,
        default: 15000
    }
});

const currentIndex = ref(0);
let timer = null;
const transitionEffect = ref('slide-next');

// 当前媒体信息
const currentMedia = computed(() => media_type(props.media_list[currentIndex.value]));

// 切换媒体
function switchMedia(index) {
    const newIndex = (index + props.media_list.length) % props.media_list.length;
    transitionEffect.value = newIndex > currentIndex.value ? 'slide-next' : 'slide-prev';
    currentIndex.value = newIndex;
    resetTimer();
}

// 自动播放
function startTimer() {
    timer = setInterval(() => {
        switchMedia(currentIndex.value + 1);
    }, props.interval);
}

function resetTimer() {
    clearInterval(timer);
    startTimer();
}

// 媒体类型判断
function media_type(url) {
    return {
        type: url.endsWith('.mp4') ? 'video' : 'img',
        url: url
    };
}

onMounted(()=>{
    startTimer();
    //store.setBgColor('#f5f1e8')
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.auto_switch_media {
    position: relative;
    max-width: calc(100% - 40px);
    width: calc(100% - 100px);
    margin: 0 auto;
    height: 100%;
}

.media_container {
    height: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.media_item {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.media_img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.media_video {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #000;
}

.indicators {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    z-index: 10;
    background-color: rgba(255,255,255,0.2);
    padding: 10px;
    border-radius: 10px;
}

.indicator {
    cursor: pointer;
    opacity: 0.6;
    transition: all 0.3s ease;
}

.indicator.active {
    opacity: 1;
    transform: scale(1.2);
}

.icon {
    width: 32px;
    height: 32px;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

/* 过渡动画 */
.slide-next-enter-active,
.slide-next-leave-active,
.slide-prev-enter-active,
.slide-prev-leave-active {
    transition: all 0.5s ease;
}

.slide-next-enter-from {
    transform: translateX(100%);
    opacity: 0;
}

.slide-next-leave-to {
    transform: translateX(-100%);
    opacity: 0;
}

.slide-prev-enter-from {
    transform: translateX(-100%);
    opacity: 0;
}

.slide-prev-leave-to {
    transform: translateX(100%);
    opacity: 0;
}
</style>