#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>

static char *buffer = NULL;
static char *buffer2 = NULL;
int atoi(char *str){
    int number=0;
    while(*str){    
        number = number*10 + *str - '0';  
        str++;  
    }
    return number;
}

void itoa(int num, char *str){ 
    int i=0; 
    int radix = 10;  // 진수 
    int deg=1; 
    int cnt = 0; 

    while(1){    // 자리수의 수를 뽑는다 
        if( (num/deg) > 0) 
            cnt++; 
        else 
            break; 
        deg *= radix; 
    } 
    deg /=radix;    // deg가 기존 자리수보다 한자리 높게 카운트 되어서 한번 나누어줌  
    // EX) 1241 ->    cnt = 4; deg = 1000; 
    for(i=0; i<cnt; i++)    {    // 자리수만큼 순회 
        *(str+i) = num/deg + '0';    // 가장 큰 자리수의 수부터 뽑음 
        num -= ((num/deg) * deg);        // 뽑은 자리수의 수를 없엠 
        deg /=radix;    // 자리수 줄임 
    } 
    *(str+i) = '\0';  // 문자열끝널.. 
}  


int sysprog_device_open(struct inode *inode, struct file *filp){

	printk(KERN_ALERT "sysprog_device open function called\n");
	return 0;
}

int sysprog_device_release(struct inode *inode,struct file *filp){

printk(KERN_ALERT "sysprog_device release function called\n");
   return 0;
}


ssize_t sysprog_device_write(struct file *filp,const char *buf, size_t count, loff_t *f_pos){

	copy_from_user(buffer,buf,1024);
	printk(KERN_ALERT "write the number %s to kernel\n",buf);
    int num1;
	int num2;
	if(buffer2 == NULL)
		itoa(0,buffer2);
	num1 = atoi(buf);
    num2 = atoi(buffer2);
	num2 += num1;
	itoa(num2,buffer2);
	return count; 

}

ssize_t sysprog_device_read(struct file *filp,char *buf, size_t count, loff_t *f_pos){
     
     copy_to_user(buf,buffer2,1024);
     printk(KERN_ALERT "read the number %s from kernel\n",buf);

	 return count;
}


static struct file_operations sys_fops = {

	.owner = THIS_MODULE,
	.read  = sysprog_device_read,
	.write = sysprog_device_write,
	.open  = sysprog_device_open,
	.release = sysprog_device_release

};

int __init sysprog_device_init(void)
{
	if(register_chrdev(240,"sysprog_device", &sys_fops)<0)
		printk(KERN_ALERT "[sysprog] driver init failed\n");
	else
		printk(KERN_ALERT "[sysprog] driver init successful\n");
    buffer = (char*)kmalloc(1024, GFP_KERNEL);
	buffer2 = (char*)kmalloc(1024, GFP_KERNEL);
	if(buffer !=NULL)
		memset(buffer, 0,1024);
    if(buffer2 !=NULL)
		memset(buffer2, 0,1024);
	return 0;
}

void __exit sysprog_device_exit(void){

	unregister_chrdev(240,"sysprog_device");
	printk(KERN_ALERT "[sysprog] driver cleanup\n");
	kfree(buffer);
    kfree(buffer2);

}

module_init(sysprog_device_init);
module_exit(sysprog_device_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Jiwoong Park");
MODULE_DESCRIPTION("This is the hello world example for device driver in system programming lecture");

