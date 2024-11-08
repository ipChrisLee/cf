#include <iostream>
#include <vector>
#include <numeric>

using i32 = int32_t;

// ========================
struct UnioFindSet {
	i32 endId_; // exclusive
	std::vector<i32> fa_;
	UnioFindSet(i32 endId) : endId_(endId), fa_(endId_, 0) {
		std::iota(fa_.begin(), fa_.end(), 0);
	}
	i32 findfa(i32 x) {
		return fa_[x] == x ? x : (fa_[x] = findfa(fa_[x]));
	}
	void unite(i32 x, i32 y) {
		fa_[findfa(x)] = findfa(y);
	}
	bool same_set(i32 x, i32 y) {
		return findfa(x) == findfa(y);
	}
};
// ========================

// https://www.luogu.com.cn/problem/P3367
int main() {
	std::ios::sync_with_stdio(false); std::cin.tie(0);
	i32 n, m;
	std::cin >> n >> m;
	UnioFindSet s(n+1);
	while(m--) {
		i32 z, a, b;
		std::cin >> z >> a >> b;
		if (z == 1) {
			s.unite(a, b);
		} else {
			if (s.same_set(a, b)) {
				std::cout << "Y\n";
			} else {
				std::cout << "N\n";
			}
		}
	}
	return 0;
}
