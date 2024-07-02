using AddressBook.ViewModels;
using System.Windows;

namespace AddressBook.Views
{
    /// <summary>
    /// Interaction logic for AddContactWindow.xaml
    /// </summary>
    public partial class AddContactWindow : Window
    {
        public AddContactWindow()
        {
            InitializeComponent();
            AddContactViewModel addContactViewModel = new AddContactViewModel();
            this.DataContext = addContactViewModel;
        }
    }
}
