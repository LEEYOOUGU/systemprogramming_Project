#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
    int number =1;
    int dev;
    char buff[1024];
    printf("Device driver test.\n");
    dev = open("/dev/init_device", O_RDWR);

    if(dev == -1)
    {
        perror("failed open because ");
        return 1;
    }
    while(number != 0)
    {
    printf("input the number\n");
    scanf("%d",&number);
    sprintf(buff,"%d",number);
    write(dev,buff,4);
    read(dev,buff,4);
    printf("accumulated number in kernel space is %s\n",buff);
    }

    close(dev);
    exit(EXIT_SUCCESS);

}


