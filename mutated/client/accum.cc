#include <algorithm>
#include <cmath>
#include <numeric>
#include <iostream>

#include "accum.hh"

// TODO: Histogram rather than all samples?

using namespace std;

void Accum::clear(void)
{
    samples_.clear();
    sorted_ = false;
}

void Accum::add_sample(uint64_t val)
{
    samples_.push_back(val);
    sorted_ = false;
}

void Accum::print_samples(void)
{
    for (auto i : samples_) {
        cout << i << endl;
    }
}

double Accum::mean(void)
{
    double avg = 0;
    double sz = size();

    for (auto i : samples_) {
        avg += double(i) / sz;
    }

    return avg;
}

double Accum::stddev(void)
{
    double avg = mean();
    double sum = 0;

    for (auto i : samples_) {
        double diff = double(i) - avg;
        sum += diff * diff;
    }

    return sqrt(sum / size());
}

uint64_t Accum::percentile(double percent)
{
    std::vector<uint64_t> samples_copy(samples_);
    sort(samples_copy.begin(), samples_copy.end());
    return samples_copy[ceil(double(size()) * percent) - 1];
}

uint64_t Accum::percentile_histogram(double percent, uint64_t cnt)
{
    if (samples_.size() == 0)
        return 0;
    uint64_t real_cnt = cnt;
    if (cnt > samples_.size())
        real_cnt = samples_.size();
    std::vector<uint64_t> samples_copy(samples_.end() - real_cnt, samples_.end());
    sort(samples_copy.begin(), samples_copy.end());
    return samples_copy[ceil(double(real_cnt) * percent) - 1];
}

uint64_t Accum::min(void)
{
    std::vector<uint64_t> samples_copy(samples_);
    sort(samples_copy.begin(), samples_copy.end());
    return samples_copy[0];
}

uint64_t Accum::max(void)
{
    std::vector<uint64_t> samples_copy(samples_);
    sort(samples_copy.begin(), samples_copy.end());
    return samples_copy[samples_copy.size() - 1];
}

vector<uint64_t>::size_type Accum::size(void) { return samples_.size(); }
