using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;

namespace Validator
{
    public partial class Form1 : Form
    {
        System.IO.StreamReader settingsFileIn;
        System.IO.StreamWriter settingsFileOut;

        public Form1()
        {
            InitializeComponent();
            try
            {
                settingsFileIn = new System.IO.StreamReader("settings.txt");
                string line = settingsFileIn.ReadLine();
                modPath.Text = settingsFileIn.ReadLine();
                line = settingsFileIn.ReadLine();
                hoi4Path.Text = settingsFileIn.ReadLine();
            }
            catch
            {
                hoi4Path.Text = "";
                modPath.Text = "";
            }

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string fModPath, fHoi4Path;
            fModPath = modPath.Text;
            fHoi4Path = hoi4Path.Text;
            Process cmd = new Process();
            cmd.StartInfo = new ProcessStartInfo();
            cmd.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            cmd.StartInfo.FileName = "cmd.exe";
            cmd.StartInfo.Arguments = "/C " + "validator.exe --" + fModPath + " --" + fHoi4Path;
            long initialTicks = DateTime.Now.Ticks; 
            cmd.Start();
            cmd.WaitForExit();
            MessageBox.Show("Validator finished, output should be in the same directory as this program! It took " + Convert.ToString((DateTime.Now.Ticks - initialTicks)/10000000F) + " seconds.", this.Text);

            try
            {
                settingsFileIn.Close();
            }
            catch
            {

            }
            settingsFileOut = new System.IO.StreamWriter("settings.txt");
            settingsFileOut.WriteLine("Input File:");
            settingsFileOut.WriteLine(fModPath);
            settingsFileOut.WriteLine("Output File:");
            settingsFileOut.WriteLine(fHoi4Path);
            settingsFileOut.Flush();
            settingsFileOut.Close();

            Application.Exit();
        }
    }
}
