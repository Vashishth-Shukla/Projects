using InventorySystem.Model;
using InventorySystem.MVVM;
using System.Collections.ObjectModel;
using System.Windows;

namespace InventorySystem.ViewModel
{
    internal class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Item> Items { get; set; }
        public RelayCommand AddCommand => new RelayCommand(execute => AddItem());
        public RelayCommand DeleteCommand => new RelayCommand(execute => DeleteItem(), canExecute => SelectedItem != null);
        public RelayCommand SaveCommand => new RelayCommand(execute => Save(), canExecute => CanSave());
        public MainWindowViewModel() 
        {
            Items = new ObservableCollection<Item>();
        }

        private Item selectedItem;

        public Item SelectedItem
        {
            get { return selectedItem; }
            set 
            { 
                selectedItem = value;
                OnPropertyChanged();
            }
        }

        private void AddItem()
        {
            Items.Add(new Item
            {
                Name = "New Item",
                SerialNumber = "xxxx",
                Quantity = 0,
            });
        }

        private void DeleteItem()
        { Items.Remove(selectedItem); }

        private void Save()
        {
            MessageBox.Show(
                messageBoxText:"This feature is comming soon!", 
                caption:"Save",
                button: MessageBoxButton.OK,
                icon: MessageBoxImage.Information);
        }

        private bool CanSave()
        { return true; }
    }
}
