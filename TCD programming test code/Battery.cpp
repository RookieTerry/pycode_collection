#include <algorithm>
#include <iostream>
struct Battery  /*定义结构体 轻量级的类*/ 
{
    float charge = 0.0f;  /* f 代表这个数据是float类型的常量，如果你直接输入1.0就是double类型 ，当你赋给float类型的时候就会抛异常了，如果你不加f，你也可以这样赋值 float amount = (float)1.0 */
};
void charge(Battery* battery/*定义结构体指针*/, float charge)
{
    battery->charge += charge;
    /x = p->a;  /*这句话的意思就是取出p所指向的结构体中包含的数据项a赋值给x*/
}
#ifndef RunTests
int main()
{
    Battery battery;
    charge(&battery, 1.0f);
    std::cout << battery.charge << std::endl;
}
#endif
