using AddressBook.Models;
using AddressBook.MVVM;
using System.Windows.Input;

namespace AddressBook.ViewModels
{
    class AddContactViewModel
    {
        public ICommand IAddContact {  get; set; }
        public string? Name {  get; set; }
        public string? Email { get; set; }
        public string? Phone {  get; set; }
        public string? Address {  get; set; }

        public AddContactViewModel()
        {
            IAddContact = new RelayCommand(AddContact, CanAddCommand);
        }

        private bool CanAddCommand(object obj)
        {
            return true;
        }

        private void AddContact(object obj)
        {
            ContactManager.AddContact(new Contact
            {
                Name = Name,
                Email = Email,
                Phone = Phone,
                Address = Address,
            });
        }
    }
}
