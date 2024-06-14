using System.ComponentModel;
using System.Windows.Input;
using TodoList.Views;

namespace TodoList.ViewModels
{
    internal class MainWindowViewModel : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        public ICommand IOpenNewWindow => new RelayCommand(OpenNewWindow);

        private void OpenNewWindow()
        {
            NewTaskWindow newTaskWindow = new NewTaskWindow();
            newTaskWindow.Show();
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
