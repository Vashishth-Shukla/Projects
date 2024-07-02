using System.Collections.ObjectModel;

namespace AddressBook.Models
{
    class ContactManager
    {
        public static ObservableCollection<Contact> ContactDatabase { get; set; } = new ObservableCollection<Contact>()
        {
            new Contact()
            {
                Name = "v1",
                Email = "v@v.com",
                Address = "bla bla bla street bla blacity",
                Phone = "1234567890"
            },
            new Contact()
            {
                Name = "v1",
                Email = "v@v.com",
                Address = "bla bla bla street bla blacity",
                Phone = "1234567890"
            },
            new Contact()
            {
                Name = "v1",
                Email = "v@v.com",
                Address = "bla bla bla street bla blacity",
                Phone = "1234567890"
            },
            new Contact()
            {
                Name = "v1",
                Email = "v@v.com",
                Address = "bla bla bla street bla blacity",
                Phone = "1234567890"
            }
        };

        public static ObservableCollection<Contact> GetContacts()
        {
            return ContactDatabase;
        }

        public static void AddContact(Contact contact)
        {
            ContactDatabase.Add(contact);
        }
    }
}
