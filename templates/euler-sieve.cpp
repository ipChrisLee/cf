#include <vector>
#include <algorithm>

using i32 = int32_t;


// ========
struct EulerSieve {
	i32 endNum_; // exclusive
	std::vector<bool> isPrime_;
	std::vector<i32> mnFactor_;
	std::vector<i32> primes_;
	EulerSieve(i32 endNum) : endNum_(endNum), isPrime_(endNum_, true), mnFactor_(endNum_, 1){
		for (i32 i=2; i<endNum_; ++i) {
			if (isPrime_[i]) {
				primes_.emplace_back(i);
			} 
			for (i32 j : primes_) {
				if (i * j >= endNum_) { break; }
				if (isPrime_[i*j]) {
					mnFactor_[i*j] = std::min(i, j);
					isPrime_[i*j] = false;
				}
				if (i % j == 0) {
					break;
				}
			}
		}
	}
	bool is_prime(i32 x) { return isPrime_[x]; }
	i32 min_factor(i32 x) { return mnFactor_[x]; }
	i32 ith_prime(i32 i) { return primes_[i]; }
};
// ========

int main() {
	return 0;
}
