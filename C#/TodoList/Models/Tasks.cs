using System;
using System.Collections.ObjectModel;

namespace TodoList.Models
{
    public class Task
    {
        public int Id { get; set; }
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


    }
    public enum TaskState
    {
        InProgress,
        Completed,
        NotStarted,
        Late,
        Archived,
        Deleted
    }

    public enum TaskCatagory
    {
        Work,
        Personal,
        Home,
        HealthWelbeing,
        Finance,
        Shopping,
        SocialFamily,
        Education,
        Travel,
        Errands,
        HobbiesLeisure,
        VolunteeringCommunity,
        BrithdaysAnniversaries,
        Projects,
        LongTermGoals
    }

    public enum TaskImportance
    {
        Low,
        Medium,
        High,
        Critical
    }
}
