using System.Windows.Input;

namespace AddressBook.MVVM
{
    public class RelayCommand : ICommand
    {
        private Action<object>? _Execute { get; set; }
        private Predicate<object>? _CanExecute { get; set; }

        public event EventHandler? CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
        public RelayCommand(Action<object> ExecuteMethod, Predicate<object> CanExecuteMethod)
        {
            _CanExecute = CanExecuteMethod;
            _Execute = ExecuteMethod;
        }
        public bool CanExecute(object? parameter)
        {
            return _CanExecute(parameter);
        }

        public void Execute(object? parameter)
        {
            _Execute(parameter);
        }
    }
}
