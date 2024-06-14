using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows.Input;
using TodoList.DataServices;
using TodoList.Models;
using TodoList.Views;

namespace TodoList.ViewModels
{
    public class TaskViewModel : INotifyPropertyChanged
    {
        private readonly TaskDataService _taskDataService;

        private ObservableCollection<Task> _tasks;

        public string Title { get; set; }
        public string Description { get; set; }
        public DateTime DueDate { get; set; }
        public DateTime StartDate { get; set; }
        public bool IsCompleted { get; set; }
        public TimeSpan Timer { get; set; }
        public TaskState TaskState { get; set; }
        public TaskCatagory TaskCatagory { get; set; }
        public TaskImportance TaskImportance { get; set; }
        public ObservableCollection<TaskChecklist> TaskChecklists { get; set; }

        public ICommand IAddNewTask => new RelayCommand(AddNewTask);
        public ICommand IClearFormFields => new RelayCommand(ClearFormFields);


        public ObservableCollection<Task> Tasks
        {
            get => _tasks;
            set
            {
                _tasks = value;
                OnPropertyChanged(nameof(Tasks));
            }

        }

        public event PropertyChangedEventHandler PropertyChanged;

        public TaskViewModel()
        {
            _taskDataService = new TaskDataService();
            TaskChecklists = new ObservableCollection<TaskChecklist>();
            DueDate = DateTime.Now;
        }

        public void LoadTasks()
        {
            var TaskList = _taskDataService.LoadTasks();
            Tasks = new ObservableCollection<Task>(TaskList);
        }

        public void AddNewTask()
        {
            Task newTask = new Task()
            {
                Title = this.Title,
                Description = this.Description,
                Id = _taskDataService.GenerateNewTaskId(),
                DueDate = DateTime.Now,
                IsCompleted = false,
                StartDate = DateTime.Now,
                TaskCatagory = TaskCatagory.Education,
                TaskChecklists = this.TaskChecklists,
                TaskImportance = TaskImportance.Critical,
                TaskState = TaskState.Late,
                Timer = new TimeSpan(0)
            };
            _taskDataService.AddTask(newTask);


            // Clear fields 
            ClearFormFields();

            // reload tasks
            LoadTasks();
        }

        public void ClearFormFields()
        {
            Title = "";
            Description = "";
            DueDate = DateTime.Now;
            TaskChecklists.Clear();

            UpdateFormView();
        }

        private void UpdateFormView()
        {
            OnPropertyChanged(Title);
            OnPropertyChanged(Description);
            OnPropertyChanged(nameof(DueDate));
            OnPropertyChanged(nameof(TaskChecklists));
        }

        public void UpdateTask(Task updatTask)
        {
            _taskDataService.UpdateTask(updatTask);
            LoadTasks();
        }

        public void DeleteTask(int taskId)
        {
            _taskDataService.DeleteTask(taskId);
            LoadTasks();
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}