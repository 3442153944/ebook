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
}