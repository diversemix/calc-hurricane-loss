// poisson_distribution
#include <iostream>
#include <random>

class EventDefinition {
  public: 
    EventDefinition(long double rate, long double mean, long double stddev ) {
      this->event_rate = rate;
      this->loss_mean = mean;
      this->loss_stddev = stddev;

      this->event_distribution = std::poisson_distribution<>(this->event_rate);
      this->loss_distribution = std::lognormal_distribution<>(this->loss_mean, this->loss_stddev);
      this->generator = std::mt19937(this->rd());
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
    long double event_rate;
    long double loss_mean;
    long double loss_stddev;
    std::random_device rd;

    // https://en.cppreference.com/w/cpp/numeric/random/poisson_distribution/poisson_distribution
    std::poisson_distribution<> event_distribution;
    std::lognormal_distribution<> loss_distribution;
    std::mt19937 generator;

};

int main() {
  const int n_years = 1e6; 

  EventDefinition * florida = new EventDefinition(10, 2.2, 0.2);
  EventDefinition * gulf = new EventDefinition(22, 1.1, 0.1);

  long double total_loss = 0;

  for (int i = 0; i < n_years; ++i) {
    total_loss += florida->loss_in_year();
    total_loss += gulf->loss_in_year();
  }

  std::cout << "Mean loss=" << total_loss / n_years 
            << " per year calculated over " << n_years << " years."
            << std::endl;

  delete florida;
  delete gulf;

  return 0;
}

