#include<iostream>
#include<vector>
std::vector findShortest(const std::vector<std::vector>& vectors)
{
    std::vector ret;
    if (vectors.empty()) return ret;
    ret = vectors[0];
    for (int i = 1; i < vectors.size(); i++)
    {
        if ((long long)ret[0] * ret[0] + ret[1] * ret[1] + ret[2] * ret[2] >
            (long long)vectors[i][0] * vectors[i][0] + vectors[i][1] * vectors[i][1] + vectors[i][2] * vectors[i][2])
        {
            ret = vectors[i];
        }
    }
    return ret;
}
