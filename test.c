int myCube(int num)
{
    return num * num * num;
}

int myPow(int num, int exp)
{
    int ret = 1;
    for (int i = 0; i < exp; i++) ret *= num;
    return ret;
}

void increment(int* x)
{
    *x += 1;
}
