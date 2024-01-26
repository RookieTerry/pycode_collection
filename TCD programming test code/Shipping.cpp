#include <stdexcept>
#include <iostream>
int minimalNumberOfPackages(int items, int availableLargePackages, int availableSmallPackages)
{
    int ans = 0;
    int itemNeedLargeNum = items / 5;
    ans += std::min(itemNeedLargeNum, availableLargePackages);
    items -= std::min(itemNeedLargeNum, availableLargePackages) * 5;
    if (items > availableSmallPackages)
    {
        return -1;
    }
    return ans + items;
}

#ifndef RunTests
int main()
{
    std::cout << minimalNumberOfPackages(16, 2, 10);
}
#endif
