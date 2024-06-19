using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace AreYouDumb
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool _firstClick = true;
        private Random _random = new Random();
        private string[] _verticalAlignment = { "Top", "Center", "Botton" };
        private string[] _horizontalAlignment = { "Left", "Center", "Right" };

        public MainWindow()
        {
            InitializeComponent();
            tbName.Text = "Are you dumb?";
            YesButton.Content = "Yes!";
        }

        private void YesButton_Click(object sender, RoutedEventArgs e)
        {
            if (_firstClick)
            {
                tbName.Text = "Well! No Worries. At least you know! ;P";
                YesButton.Content = "Try Again!";
            }
            else
            {
                tbName.Text = "Are you dumb?";
                YesButton.Content = "Yes!";
            }
            _firstClick = !_firstClick;
        }

        private void NoButton_IsMouseDirectlyOverChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            int verticalIndex = _random.Next(0, _verticalAlignment.Length);
            int horizontalIndex = _random.Next(0, _horizontalAlignment.Length);

            VerticalAlignment verticalAlignmentEnum;
            HorizontalAlignment horizontalAlignmentEnum;

            if (Enum.TryParse(_verticalAlignment[verticalIndex], out verticalAlignmentEnum) &&
                Enum.TryParse(_horizontalAlignment[horizontalIndex], out horizontalAlignmentEnum))
            {
                NoButton.VerticalAlignment = verticalAlignmentEnum;
                NoButton.HorizontalAlignment = horizontalAlignmentEnum;
            }
        }
    }
}