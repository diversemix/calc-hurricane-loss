// poisson_distribution
#include <iostream>
#include <random>
#include <thread>
#include <mutex>

class EventDefinition {
  public: 
    EventDefinition(long double rate, long double mean, long double stddev ) {
      this->initialise(rate, mean, stddev);
    }

    EventDefinition(const EventDefinition & right) {
      this->initialise(right.event_rate, right.loss_mean, right.loss_stddev);
    }

    long double loss_in_year() {

      long double total = 0;
      int num_events = this->event_distribution(this->generator);
      for (int i = 0; i < num_events; i++)
      {
        total += this->loss_distribution(this->generator); 
      }

      return total;
    }

  private:
    void initialise(long double rate, long double mean, long double stddev) {
      this->event_rate = rate;
      this->loss_mean = mean;
      this->loss_stddev = stddev;

      this->event_distribution = std::poisson_distribution<>(this->event_rate);
      this->loss_distribution = std::lognormal_distribution<>(this->loss_mean, this->loss_stddev);
      this->generator = std::mt19937(this->rd());
    }

    long double event_rate;
    long double loss_mean;
    long double loss_stddev;
    std::random_device rd;

    // https://en.cppreference.com/w/cpp/numeric/random/poisson_distribution/poisson_distribution
    std::poisson_distribution<> event_distribution;
    std::lognormal_distribution<> loss_distribution;
    std::mt19937 generator;

};

int multi_calculator(int n_years, EventDefinition & florida, EventDefinition & gulf) {
  unsigned num_cpus = std::thread::hardware_concurrency();
  std::cout << "Launching " << num_cpus << " threads\n";

  std::vector<std::thread> threads(num_cpus);
  std::vector<long double> results(num_cpus);

  std::mutex iomutex;
  for (unsigned i = 0; i < num_cpus; ++i) {
    
    threads[i] = std::thread([&iomutex, i, num_cpus, &results, n_years, florida, gulf] {
        {
          std::lock_guard<std::mutex> iolock(iomutex);
          std::cout << "Thread #" << i << ": on CPU " << sched_getcpu() << "\n";
        }      
      EventDefinition newFlorida = EventDefinition(florida);
      EventDefinition newGulf = EventDefinition(gulf);
      long double total_loss = 0;
      
      for (int i = 0; i < int(n_years / num_cpus); ++i) {
        total_loss += newFlorida.loss_in_year();
        total_loss += newGulf.loss_in_year();
      }

      results[i] = total_loss;
    });
  }

  for (auto& t : threads) {
    t.join();
  }
  long double total_loss = 0;
  for (auto it : results) {
    total_loss += it;
  }

  return total_loss;
}


// long double single_calculator(int n_years, EventDefinition & florida, EventDefinition & gulf) {

//   long double total_loss = 0;
  
//   for (int i = 0; i < n_years; ++i) {
//     total_loss += florida.loss_in_year();
//     total_loss += gulf.loss_in_year();
//   }

//   return total_loss;
// }

int main() {
  const int n_years = 1e6; 

  EventDefinition florida = EventDefinition(10, 2.2, 0.2);
  EventDefinition gulf = EventDefinition(22, 1.1, 0.1);

  // long double total_loss = single_calculator(n_years, florida, gulf);
  long double total_loss = multi_calculator(n_years, florida, gulf);
  
  std::cout << "Mean loss=" << total_loss / n_years 
            << " per year calculated over " << n_years << " years."
            << std::endl;


  return 0;
}

