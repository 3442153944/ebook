export class BaseApi {
    private base_url: string
    private token: string
    constructor(base_url: string = 'http://localhost:8000/') {
        this.base_url = base_url;
        this.token = this.get_token();
      }
    private get_token(): string{
        return  localStorage.getItem('token') || ''
    }

    public async post(api = '', data: Object): Promise<{result:Object, status:number}>{
        try {
            const token = this.get_token()
            const res = await fetch(this.base_url + api, {
                method: 'POST',
                headers: {
                    'Authorization': `token ${token}`
                },
                body: JSON.stringify(data)
            })
            const result = await res.json()
            console.log(result)
            const status = res.status
            return { result, status }
        }
        catch (err) {
            console.log(err)
            return { result: {}, status: 500 }
        }

    }
    //一些常用的api
    public async get_user_info_by_id(id:string):Promise<{result:Object, status:number}>{
        try{
            return this.post('api/user/get_user_info_by_id', {target_id:id})
        }
        catch(err){
            console.log(err)
            return {result:{}, status:500}
        }
    }
    public async get_notice_by_id(send_user_id:string,limit:number=10,offset:number=0):Promise<{result:Object, status:number}>{
        return this.post('api/user/get_notice_by_id',{
            send_user_id:send_user_id,
            limit:limit,
            offset:offset
        })
    }
    //通用时间格式化函数
    public formatTimeAgo(dateTimeStr: string): string {
        // 统一处理两种时间格式
        const standardized = dateTimeStr.replace('T', ' ');
        const targetTime = new Date(standardized);
        const now = new Date(); 
        
        // 时间差（毫秒）
        const diff = now.getTime() - targetTime.getTime();
        const seconds = Math.floor(diff / 1000);
        
        // 时间单位计算
        const intervals = {
          年: 31536000,
          月: 2592000, // 按30天算
          周: 604800,
          天: 86400,
          小时: 3600,
          分钟: 60,
          秒: 1
        };
      
        // 超过1个月（按30天算）显示具体日期
        if (diff > 30 * 24 * 3600 * 1000) {
          return `${targetTime.getFullYear()}年${
            targetTime.getMonth() + 1}月${targetTime.getDate()}日`;
        }
      
        // 计算相对时间
        let counter;
        for (const [unit, secondsInUnit] of Object.entries(intervals)) {
          counter = Math.floor(seconds / secondsInUnit);
          if (counter > 0) {
            if (unit === '月') { // 单独处理月
              return counter + unit + '前';
            }
            return counter + unit + (counter > 1 ? '' : '') + '前';
          }
        }
        
        return '刚刚';
      }
      public change_img(node: HTMLImageElement, file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            // 增强类型校验
            if (!(node instanceof HTMLImageElement)) {
                return reject(new Error('Invalid image element'))
            }
            if (!(file instanceof File)) {
                return reject(new Error('Invalid File object'))
            }
            // 扩展文件类型校验
            const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
            if (!ALLOWED_TYPES.includes(file.type)) {
                return reject(new Error(`Unsupported image type: ${file.type}`))
            }
            // 内存管理
            const revokePreviousURL = () => {
                if (node.src.startsWith('blob:')) {
                    URL.revokeObjectURL(node.src)
                }
            }
            const reader = new FileReader()
            reader.onload = (e) => {
                revokePreviousURL()
                const result = e.target?.result
                if (typeof result !== 'string') {
                    return reject(new Error('Failed to read file as DataURL'))
                }
                // 添加临时加载状态
                node.style.opacity = '0.5'
                const handleLoad = () => {
                    node.style.opacity = '1'
                    resolve(result)
                }
                const handleError = () => {
                    node.style.opacity = '1'
                    reject(new Error('Failed to load image'))
                }
                node.addEventListener('load', handleLoad, { once: true })
                node.addEventListener('error', handleError, { once: true })
                node.src = result
            }
            reader.onerror = () => {
                reject(new Error(`File read error: ${reader.error?.message}`))
            }
            try {
                reader.readAsDataURL(file)
            } catch (error) {
                reject(new Error(`File read failed: ${error}`))
            }
        })
    }
}