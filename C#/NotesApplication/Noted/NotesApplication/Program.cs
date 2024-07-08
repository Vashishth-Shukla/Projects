using NotesApplication;
using NotesApplication.Commands;


using var dbContext = new AppDbContext();

var commands = new Dictionary<string, ICommand>
                {
                    {"list", new ListNotesCommand(dbContext) },
                    {"create", new CreateNoteCommand(dbContext)},
                    {"read", new ReadNoteCommand(dbContext)},
                    {"update", new UpdateNoteCommand(dbContext)},
                    {"delete", new DeleteNoteCommand(dbContext)},
                    {"search", new SearchNoteCommand(dbContext)}
                };

while (true)
{
    Console.Clear();

    Console.WriteLine("Let's note what not Noted!");

    Console.WriteLine("Your console command is my command!");

    Console.WriteLine("Enter a command : ");

    var commandName = Console.ReadLine();

    if (commandName == "quit")
    {
        break;
    }

    if (commands.TryGetValue(commandName, out var command))
    {
        command.Execute();

        Console.WriteLine("Press any key to continue...");
        Console.ReadKey();
    }
    else
    {
        Console.WriteLine($"Unknown command : {commandName}");
        Console.WriteLine("Press any key to continue...");
        Console.ReadKey();

    }
}