// poisson_distribution
#include <iostream>
#include <random>

class EventDefinition {
  public: 
    EventDefinition(long double rate, long double mean, long double stddev ) {
      this->event_rate = rate;
      this->loss_mean = mean;
      this->loss_stddev = stddev;
    }

    long double loss_in_year() {
      std::mt19937 gen(this->rd());
      // double gen = 1;

      std::poisson_distribution<int> d_events(this->event_rate);
      std::lognormal_distribution<> d_loss(this->loss_mean, this->loss_stddev);

      long double total = 0;
      int num_events = d_events(gen);
      for (int i = 0; i < num_events; i++)
      {
        total += d_loss(gen); 
      }

      return total;
    }

  private:
    long double event_rate;
    long double loss_mean;
    long double loss_stddev;

    std::random_device rd;

};

int main() {
  const int n_years = 100000; 

  EventDefinition * florida = new EventDefinition(10, 2.2, 0.2);
  EventDefinition * gulf = new EventDefinition(22, 1.1, 0.1);

  long double total_loss = 0;

  for (int i = 0; i < n_years; ++i) {
    total_loss += florida->loss_in_year();
    total_loss += florida->loss_in_year();

  }

  std::cout << "Mean loss=" << total_loss / n_years 
            << " per year calculated over " << n_years << " years."
            << std::endl;

  delete florida;
  delete gulf;

  return 0;
}

