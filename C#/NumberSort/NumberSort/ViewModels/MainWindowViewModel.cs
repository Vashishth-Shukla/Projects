using NumberSort.Models;
using NumberSort.MVVM;
using System.Collections;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Windows;

namespace NumberSort.ViewModels
{
    class MainWindowViewModel : ViewModelBase
    {
        public RelayCommand IAddNumber => new RelayCommand(ExecuteMethod => AddToRawList(), CanExecuteMethod => (RawList==null || RawList.Count <= 20) && AddNumber != null && selectedNumber == null);
        public RelayCommand IDeleteNumber => new RelayCommand(ExecuteMethod => DeleteNumber(), CanExecuteMethod => selectedNumber != null);
        public RelayCommand IPolulateRawList => new RelayCommand(
            ExecuteMethod => PolulateRawList(), 
            CanExecuteMethod => int.TryParse(ListLength.ToString(), out int number) && number >= 1 && number <= 20);
        public RelayCommand ISortList => new RelayCommand(ExecuteMethod => SortRawList(), CanExecuteMethod => RawList!=null && RawList.Count >0 && RepeatSortNumber != null);
        public RelayCommand IRandomDisplayNumber => new RelayCommand(ExecuteMethod => RandomDisplayNumber(), CanExecuteMethod => true);


        public ObservableCollection<NumberModel> rawList;
        public ObservableCollection<NumberModel> RawList
        {
            get { return rawList; }
            set
            {
                rawList = value;
                OnPropertyChanged(nameof(RawList));
            }
        }

        public Dictionary<int, ObservableCollection<NumberModel>> sortResult {  get; set; }
        private ObservableCollection<string> sortedList;
        public ObservableCollection<string> SortedList
        {
            get
            {
                return sortedList;
            }
            set
            {
                sortedList = value;
                OnPropertyChanged(nameof(SortedList));
            }
        }

        public int? AddNumber { get; set; }
        public int ListLength {  get; set; }
        private int? repeatSortNumber;
        public int? RepeatSortNumber
        {
            get
            {
                return repeatSortNumber;
            }
            set
            {
                repeatSortNumber = value;
                OnPropertyChanged(nameof(RepeatSortNumber));
            }
        }
        private int? showListNumber;
        public int? ShowListNumber
        {
            get
            {
                return showListNumber;
            }
            set
            {
                showListNumber = value;
                OnPropertyChanged(nameof(ShowListNumber));
            }
        }
        
        private string statusMessage;
        public string? StatusMessage  // needs some fixing.
        {
            get
            {
                return statusMessage;
            }
            set
            {
                statusMessage = value;
                OnPropertyChanged(nameof(StatusMessage));
            }
        }

        private TimeSpan elapsedTime;
        public TimeSpan ElapsedTime
        {
            get { return elapsedTime; }
            set
            {
                elapsedTime = value;
                OnPropertyChanged(nameof(ElapsedTime));
            }
        }

        private bool enables;
        public bool Enables
        {
            get { return enables; }
            set
            {
                enables = value;
                OnPropertyChanged(nameof(Enables));
            }
        }
        // Selected Number
        private NumberModel? selectedNumber;
        public NumberModel? SelectedNumber
        {
            get { return selectedNumber; }
            set
            {
                SelectedNumber = value;
                OnPropertyChanged();
            }
        }

        //constructor 
        public MainWindowViewModel()
        {
            RawList = new ObservableCollection<NumberModel>();
            SortedList = new ObservableCollection<string>();
            AddNumber = null;
            sortResult = new Dictionary<int, ObservableCollection<NumberModel>>();
            ListLength = 10; // Default value, adjust as needed
            RepeatSortNumber = 10000;
            ShowListNumber = 1234;
            ElapsedTime = TimeSpan.Zero;
            StatusMessage = "Ready!";
            Enables = true;
        }

        // Add number
        private void AddToRawList()
        {
            if (int.TryParse(AddNumber.ToString(), out int number) && number >= 1 && number <= 20 && !RawList.Any(n => n.Value == number))
            {
                RawList.Add(new NumberModel { Value = number });
                StatusMessage = "Number added successfully.";
            }
            else
            {
                MessageBox.Show(
                    messageBoxText: "Please enter a unique integer between 1 and 20!",
                    caption:"Input Error!", 
                    button: MessageBoxButton.OK, 
                    icon: MessageBoxImage.Error);
                StatusMessage = "Invalid input. Please enter a unique number between 1 and 20.";
            }
        }


        // Delete Number
        private void DeleteNumber()
        {
            RawList.Remove(selectedNumber);
            StatusMessage = "Number Deleted Successfully!";
        }

        // Populate Raw List

        private void PolulateRawList()
        {
            RawList = new ObservableCollection<NumberModel>();
            Random random = new Random();
            var numbers = Enumerable.Range(1, 20).OrderBy(x => random.Next()).Take(ListLength).ToList();
            foreach (var number in numbers)
            {
                RawList.Add(new NumberModel { Value = number });
            }
            StatusMessage = "Raw List pupulated Successfully!";

        }

        // Sort List 

        private void SortRawList()
        {
            // disable other inputs 
            Enables = false;
            StatusMessage = "Starting to Sort.";

            ObservableCollection<NumberModel> rawList = RawList;
            ObservableCollection<NumberModel> sortList = new ObservableCollection<NumberModel>();
            Stopwatch stopwatch = new Stopwatch();

            sortResult = new Dictionary<int, ObservableCollection<NumberModel>>();

            StatusMessage = "Checking the Repeat Sort number.";
            
            // check the input RepeatSortNumber
            if (int.TryParse(RepeatSortNumber.ToString(), out int repeatSortNumber) )
            {
                StatusMessage = $"Repeat Sort Number: {repeatSortNumber}";
            }
            else
            {
                MessageBox.Show(
                    messageBoxText: "Please enter a non zero integer as the Repeat Sort Number.",
                    caption: "Input Error!",
                    button: MessageBoxButton.OK,
                    icon: MessageBoxImage.Error);
                StatusMessage = "Invalid input. Please enter a non zero integer as the Repeat Sort Number.";
            }
            
            
            // check the input ShowListNumber
            if (int.TryParse(ShowListNumber.ToString(), out int showListNumber) && showListNumber > 0 && showListNumber < repeatSortNumber)
            {
                StatusMessage = $"Repeat Sort Number: {showListNumber}";
            }
            else
            {
                MessageBox.Show(
                    messageBoxText: $"Please enter an integer between 1 and {repeatSortNumber} for Show List Number.",
                    caption: "Input Error!",
                    button: MessageBoxButton.OK,
                    icon: MessageBoxImage.Error);
                StatusMessage = $"Invalid input. Please enter an integer between 1 and {repeatSortNumber} for Show List Number.";
            }


            // time Starts Now 
            StatusMessage = "Starting to Sort.";
            

            stopwatch.Start();

            for (int i = 0; i < RepeatSortNumber; i++)
            {
                StatusMessage = $"Sorting {i+1}th time.";

                sortList = ListSorter.MergSort(RawList);
                sortResult.Add(i, sortList);
            }

            stopwatch.Stop();

            ElapsedTime = stopwatch.Elapsed;
            // time Ends Now 
            StatusMessage = "Sorting Finished.";

            int showNum = ShowListNumber ?? 1;

            int[] numbers = sortResult[showNum].Select(n => n.Value).ToArray();
            SortedList = new ObservableCollection<string>(numbers.Select(n => $"Zahl {n}"));
            // enables other inputs 
            Enables = true;
            StatusMessage = $"Showing the {showNum}th Result.";
        }

        private void RandomDisplayNumber()
        {
            Random random = new Random();
            ShowListNumber = random.Next(0, RepeatSortNumber ?? 1); 
        }
        

    }
}
