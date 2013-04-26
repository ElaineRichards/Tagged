# A challenge: Develop a web application to run on httpd, tomcat or 
# rails (using your language of choice) to list a cluster of servers 
# which come from a file or database, and each server with running/down 
# status which has been cached in a file or database.

require CGI;
my $page = CGI->new;

# File with the list of servers
my $serverlist = "serverlist";

# File with the status of the servers
my $serverstatus = "serverstatus";

# This can accumulate multiple error messages. I like to let my apps run
# to show multiple error conditions, rather than just stop on the first
# error.

my $erroraccumulator = "";

#
# Handle problems with the two input files.
#
sub reportfileerror() {
	my $filename = $_[0];
	if (!( $filename )) {
		print "Internal error in $0: reportfileerror\n";
		}
		else {
		print "Unable to open file $filename\n";
		}
	print $page->end_html;
	exit;
	}

# Start putting up the page

print $page->header();
print $page->start_html("Server Status");

# Is our data good? ie. Two files should exist

open (SERVERLIST,"serverlist") || &reportfileerror("serverlist");
if (!(open (SERVERSTATUS,"serverstatus"))) {
	close SERVERLIST;
	&reportfileerror("serverstatus");
	}

# Since this is a small project, statuses get loaded into a hash.

my %serverstatus = ();
my $n = 0;

while (<SERVERSTATUS>) {
	$n++;
	chomp;
	(my $name,my $status) = split(/\s+/);
	if (( $name ) && ( $status ))
		{
		$serverstatus{$name} = $status;
		}
		else
		{
		$erroraccumulator .= "ERROR in server status report at line $n:$_\n";
		}
	}
close SERVERSTATUS;

# The simple list of servers goes in an array.
# NOTE: If there are repeats in a given list of files, then this would have
# to go into a hash and then the keys would be put into an array.

@serverlist = ();
while (<SERVERLIST>)
	{
	chomp;
	($_) && (push (@serverlist,$_));
	}
close SERVERLIST;

# Files can be opened. Set up the status report.

(@serverlist) ||
	print "<BR>ERROR: No server list from $serverlist.";

(%serverstatus) ||
	print "<BR>ERROR: No server list from $serverstatus.";

# Start writing the table.

print $page->start_table();
print "<TR><TH>Server</TH><TH>Status</TH></TR>\n";

foreach my $server (@serverlist)
	{
	my $status = $serverstatus{$server};
	( $status ) || ( $status = "UNKNOWN" );
	print "<TR><TD> $server </TD><TD>".$status."</TD></TR>\n";
	$status = '';
	}

print $page->end_table();

#
# If any errors accumulated during the run, print them here at the bottom.
#
if ( $erroraccumulator ) {
	print "<BR>ERRORS:<BR>";
	print $erroraccumulator;
	}

print "<BR><BR> The source for this page can be seen ";
print "<a href=\"./servers.txt\">here.</a><BR>";
print "The server list file can be seen ";
print "<a href=\"./serverlist\">here.</a><BR>";
print "The server status file can be seen ";
print "<a href=\"./serverstatus\">here.</a><BR>";
print $page->end_html;
