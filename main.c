#include "stdio.h"
struct String{
    char str[1024];
    unsigned int len;
    char buf;
};
struct String input(char block,struct String data){
    while((data.buf = getchar())!=block){
        data.str[data.len++] = data.buf;
    }
    return data;
}
int main(){
    struct String data;
    data.len = 0;
    data.buf = '\0';
    data = input('\0',data);
    printf("%s\n", data.str);
}

i[10] = {1,2,3,"\n"};
u[10] = {1,2,3};
strcmp() == 1;


