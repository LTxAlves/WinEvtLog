using System;
using System.Diagnostics;
using System.Data.SqlClient;
using System.Data;

class MySample {
    // Connection parameters to database
    private static string cs = @"Server=localhost\SQLEXPRESS;Database=testdb;Trusted_Connection=True;";
    private static SqlConnection con = new SqlConnection(cs);

    public static void OpenSQLConnection() {

        if(con.State == ConnectionState.Closed) {
            con.Open();
        }

    }

    public static void CloseSQLConnection() {

        if(con.State == ConnectionState.Open) {
            con.Close();
        }

    }

    public static void DBStoreEntry(EventLogEntry entry) {

        if(OperatingSystem.IsWindows()) {
            string query = "INSERT INTO table(source, type, message) VALUES(@source, @type, @message, @time, @eventId)";
            using SqlCommand cmd = new SqlCommand(query, con);

            cmd.Parameters.Add(new SqlParameter("@source", SqlDbType.VarChar, 255)).Value=entry.Source;
            cmd.Parameters.Add(new SqlParameter("@type", SqlDbType.VarChar, 255)).Value=entry.EntryType;
            cmd.Parameters.Add(new SqlParameter("@message", SqlDbType.VarChar, 255)).Value=entry.Message;
            cmd.Parameters.Add("@time", SqlDbType.DateTime).Value=entry.TimeGenerated;
            cmd.Parameters.Add("@eventId", SqlDbType.BigInt).Value=entry.InstanceId;
            cmd.Prepare();

            int rows = cmd.ExecuteNonQuery();

            Console.WriteLine(rows + " rows inserted");
        }
        
    }

    public static void GetEventLogs(string logName = "System") {

        // OpenSQLConnection();

        // Event logs are Windows specific.
        if(OperatingSystem.IsWindows()) {
            // get System logs
            EventLog log = new EventLog(logName); //Sytem, Application, Security, Setup, or a custom event log

            // DateTime dt = DateTime.Now.AddDays(-2);

            foreach (EventLogEntry entry in log.Entries)
            {
                /* other examples of filtering entries */
                if (entry.Source.IndexOf("Update") != -1)
                // if (entry.TimeGenerated > dt)
                // if (entry.Source.Equals(".NET Runtime 2.0 Error Reporting") && (entry.TimeGenerated > dt))
                {
                    Console.WriteLine(entry.Source);
                    Console.WriteLine("\t" + entry.EntryType);
                    Console.WriteLine("\t" + entry.Message);
                    Console.WriteLine("\tEntry ID: " + entry.InstanceId);
                    Console.WriteLine("\tTimestamp: " + entry.TimeGenerated);
                    Console.WriteLine("--------");
                }

                // DBStoreEntry(entry);
            }

            // CloseSQLConnection();
            
            Console.WriteLine("Done");
        }
    }

    public static void Main() {

        GetEventLogs("System");
    }
}