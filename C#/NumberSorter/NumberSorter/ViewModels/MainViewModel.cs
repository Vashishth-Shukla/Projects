using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Input;
using System.Diagnostics;
using NumberSorter.Models;

namespace NumberSorter.ViewModels
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private const int N = 10000;
        private ObservableCollection<NumberEntry> rawList;
        private ObservableCollection<NumberEntry> sortedList;
        private string inputNumbers;
        private string timeTaken;
        private string statusMessage;
        private bool isSorting;

        public ObservableCollection<NumberEntry> RawList
        {
            get => rawList;
            set { rawList = value; OnPropertyChanged(nameof(RawList)); }
        }

        public ObservableCollection<NumberEntry> SortedList
        {
            get => sortedList;
            set { sortedList = value; OnPropertyChanged(nameof(SortedList)); }
        }

        public string InputNumbers
        {
            get => inputNumbers;
            set { inputNumbers = value; OnPropertyChanged(nameof(InputNumbers)); }
        }

        public string TimeTaken
        {
            get => timeTaken;
            set { timeTaken = value; OnPropertyChanged(nameof(TimeTaken)); }
        }

        public string StatusMessage
        {
            get => statusMessage;
            set { statusMessage = value; OnPropertyChanged(nameof(StatusMessage)); }
        }

        public bool IsSorting
        {
            get => isSorting;
            set { isSorting = value; OnPropertyChanged(nameof(IsSorting)); }
        }

        public ICommand AddNumberCommand { get; }
        public ICommand SortNumbersCommand { get; }
        public ICommand ResetCommand { get; }

        public MainViewModel()
        {
            RawList = new ObservableCollection<NumberEntry>();
            SortedList = new ObservableCollection<NumberEntry>();
            AddNumberCommand = new RelayCommand(AddNumber, CanAddNumber);
            SortNumbersCommand = new RelayCommand(SortNumbers, CanSortNumbers);
            ResetCommand = new RelayCommand(Reset);
        }

        private void AddNumber()
        {
            try
            {
                var numbers = InputNumbers.Split(',').Select(int.Parse).Distinct().ToList();
                if (numbers.Any(n => n < 1 || n > 20))
                {
                    StatusMessage = "Numbers must be between 1 and 20.";
                    return;
                }

                RawList.Clear();
                foreach (var number in numbers)
                {
                    if (RawList.Any(n => n.Number == number))
                    {
                        StatusMessage = $"Number {number} is already in the list.";
                        return;
                    }
                    RawList.Add(new NumberEntry(number));
                }
                StatusMessage = "Numbers added successfully.";
            }
            catch (Exception)
            {
                StatusMessage = "Invalid input. Please enter numbers separated by commas.";
            }
        }

        private bool CanAddNumber()
        {
            return !IsSorting;
        }

        private void SortNumbers()
        {
            IsSorting = true;
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();

            for (int i = 0; i < N; i++)
            {
                var sorted = RawList.OrderBy(x => x.Number).ToList();
                SortedList = new ObservableCollection<NumberEntry>(sorted);
            }

            stopwatch.Stop();
            TimeTaken = $"Time Taken: {stopwatch.ElapsedMilliseconds} ms";
            StatusMessage = "Sorting completed.";
            IsSorting = false;
        }

        private bool CanSortNumbers()
        {
            return RawList.Count > 0 && !IsSorting;
        }

        private void Reset()
        {
            RawList.Clear();
            SortedList.Clear();
            InputNumbers = string.Empty;
            TimeTaken = string.Empty;
            StatusMessage = "Reset completed.";
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
