using AddressBook.Models;
using AddressBook.MVVM;
using AddressBook.Views;
using System.Collections.ObjectModel;
using System.Windows;

namespace AddressBook.ViewModels
{
    class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Contact>? Contacts { get; set; }

        public RelayCommand IShowAddContactWindow { get; set; }

        public RelayCommand IDeleteContact => new RelayCommand(ExecuteMethod => DeleteContact(), CanExecuteMethod => selectedContact != null);
        private Contact selectedContact;
        public Contact SelectedContact 
        { 
            get { return selectedContact; }
            set 
            {
                selectedContact = value; 
                OnPropertyChanged();
            } 
        }

        public MainWindowViewModel()
        {
            Contacts = ContactManager.GetContacts();
            IShowAddContactWindow = new RelayCommand(ShowAddContactWindow, CanShowAddContactWindow);
        }

        private void DeleteContact()
        {
            Contacts.Remove(selectedContact);
        }

        private bool CanShowAddContactWindow(object obj)
        {
            return true;
        }

        private void ShowAddContactWindow(object obj)
        {
            var mainWindow = obj as Window;
            AddContactWindow addContactWindow = new AddContactWindow();
            addContactWindow.Owner = mainWindow;
            addContactWindow.WindowStartupLocation = WindowStartupLocation.CenterOwner;
            addContactWindow.Show();
        }
    }
}
