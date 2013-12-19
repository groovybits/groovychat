#!/usr/bin/perl
#
# chat.cgi -- Groovy-Chatter CGI 
# Copyright (C) 1997, 1998, 1999, 2000 
# Christopher T. Kennedy <getdown@groovy.org>
#    
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#############################################################################
$VERSION = "1.4.1"; 

use DBI;
$row=13;

# Print the Content Type.
####################################
print "Content-type: text/html\n\n";

# Persons Room Name And Script Location.
$cfg = 1;

push (@INC,`pwd`);
require 'chat.cfg' || 
	die "The Configuration File Could Not Be Found: $!\n";

if ($cfg == 1) { 
   ##########################
   # Configurable Variables #
   ##########################
   $MAIN_TITLE = "Chat Room";
   $EXIT_URL = "/";
   $ERS_INT = 10;
   $BCOLOR = "";
   $TBCOLOR = "";
   $CHATBACK = "";
   $LINK = "";
   $VLINK = "";
   $TEXT = "";
   $TTEXT = "";
   $TTEXT = "";
   $CHAT_TXT = "";
   $B_TEXT = "";
   $E_TEXT = "";
   $ALERT_COLOR = "";

   $ADM_MAIL = "";
   $BACKGROUND = " BGCOLOR=\"$BCOLOR\" ";
   $CBOXCOLOR = $BCOLOR;
   $IMG = "";
   $IMG_URL = "";
   $IMG_URL_TXT = "";
   #################################
   # End of Configurable Variables #
   #################################
}

# Numbers For Logging Lengths
$CHAT_LENGTH = 100;
$NMSTART = 1000;
$MAX_NAME = 100000;
$MAX_LOG = 100;

$TITLE = "Welcome to the $MAIN_TITLE";
$ENTER_MSG = "Entered $MAIN_TITLE";
$PG_POS = "#bottom";
$BIN_CGI = "chat.cgi";
$LOG_FILE = "chatbase";
$NOTIFY = 0;

######################
# Subroutines To Run #
######################

$|=1;

&main;

############

# Main Body #
#############
sub main
{
   # Read User Input From CGI Post
   @c_entry = split(/&/, <STDIN>);

   foreach $i (0 .. $#c_entry) {
      # Convert Plus Signs to Spaces
      $c_entry[$i] =~ s/\+/ /g;
   
      # Convert Hex to Char
      $c_entry[$i] =~ s/%(..)/pack("c", hex($1))/ge;
      
      # Censor Out Bad Characters Like HTML and colons
      $c_entry[$i] =~ s/<//ge;
      $c_entry[$i] =~ s/>//ge;

      # Let somebody do HTML if they know the code...
      #$c_entry[$i] =~ s/_SX_/'<'/ge;
      #$c_entry[$i] =~ s/_EX_/'>'/ge;

      if ( $c_entry[$i] =~ / httpCOLPPP/ ) {
         @b_entry = split(/ /, $c_entry[$i]);

         foreach $j (0 .. $#b_entry) {
            if ( $b_entry[$j] =~ /httpCOLPPP/ ) {
               ($ahttp, $aspace, $aurl) = split(/\//, $b_entry[$j], 3);
               $a_entry[$j] = " <AHREFE$b_entry[$j]>$b_entry[$j]</A> ";
               $a_entry[$j] =~ s/body=/ /e; 

               $c_entry[$i] =~ s/ httpCOLPPP/$a_entry[$j] /e; 
               $c_entry[$i] =~ s/ \/\/$aurl//e; 
            }
         }
      }
   
      # Split into name and value
      ($name, $value) = split(/=/, $c_entry[$i], 2);

      # Create the associative element
      $c_entry{$name} = $value;
   }

   $c_entry{"name"} =~ s/^0/_0/e; 
   $c_entry{"name"} =~ s/^1/_1/e; 
   $c_entry{"name"} =~ s/^2/_2/e; 
   $c_entry{"name"} =~ s/^3/_3/e; 
   $c_entry{"name"} =~ s/^4/_4/e; 
   $c_entry{"name"} =~ s/^5/_5/e; 
   $c_entry{"name"} =~ s/^6/_6/e; 
   $c_entry{"name"} =~ s/^7/_7/e; 
   $c_entry{"name"} =~ s/^8/_8/e; 
   $c_entry{"name"} =~ s/^9/_9/e; 

   # Open Chat DataBase For Access
   ################################
   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword)|| 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";
   $c_entry{$name} = $value;
   $remote="$ENV{'REMOTE_ADDR'}.$c_entry{name}";
   $sth=$dbh->prepare("select * from $btable where main='$remote' and name='$c_entry{$name}'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
   $sth->execute() ||
          die "Bad Execute $sth::errstr\n";
    while (($row = $sth->fetchrow_arrayref))
    {
      $amnths=$row->[0];
      $amday=$row->[1];
      $ahour=$row->[2];
      $amin=$row->[3];
      $asec=$row->[4];
      $aurl=$row->[5];
      $asize=$row->[6];
      $acolor=$row->[7];
      $ahurl=$row->[8];
      $aname=$row->[9];
      $apasswd=$row->[10];
      $abody=$row->[11];
      $auserno=$row->[12];
      $amain=$row->[13];
    }
    $dbh->disconnect;

   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$aname'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";

    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";

    while (($row = $sth->fetchrow_arrayref))
    {
      $u_mnths=$row->[0];
      $u_mday=$row->[1];
      $u_hour=$row->[2];
      $u_min=$row->[3];
      $u_sec=$row->[4];
      $u_url=$row->[5];
      $u_size=$row->[6];
      $u_color=$row->[7];
      $u_hurl=$row->[8];
      $u_name=$row->[9];
      $u_passwd=$row->[10];
      $u_body=$row->[11];
      $u_userno=$row->[12];
      $u_main=$row->[13];
    }

   $dbh->disconnect;

   # Entry if User Input is NULL (entering). 
   #########################################
   if ( $c_entry{"name"} eq "" ) { 

      &enterChat;

      # If trying to enter without a NAME alert them.
      ###############################################
      if ($c_entry{"body"} eq $ENTER_MSG) 
      {
print <<END;
  <P ALIGN=CENTER>
  <FONT SIZE=5 COLOR=$ALERT_COLOR>
  <B><I>Please Pick a Nick Name!</I></B>
  </FONT>
  </P>
END
      }
      
     exit 0;
   }

   # Calculate the local time. 
   &localTime;

    $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$c_entry{\"name\"}'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";

    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";

    while (($row = $sth->fetchrow_arrayref))
    {
      $mnths=$row->[0];
      $mday=$row->[1];
      $hour=$row->[2];
      $min=$row->[3];
      $sec=$row->[4];
      $url=$row->[5];
      $size=$row->[6];
      $color=$row->[7];
      $hurl=$row->[8];
      $name=$row->[9];
      $passwd=$row->[10];
      $body=$row->[11];
      $userno=$row->[12];
      $main=$row->[13];
    }
    $dbh->disconnect;

   if ($userno eq "") {

    $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
        die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where name='<nousers>'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";

    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";

    while (($row = $sth->fetchrow_arrayref))
    {
      $nousers=$row->[12];
    }
    
    if ($nousers eq '') {
      $nousers=0;
    }

    $userno = $nousers + 1000;

    $dbh->do("delete from $btable where name='<nousers>'") ||
            die "Bad response from $host Deleting:\n$dbh::errstr\n";

    $dbh->do("insert into $btable values ('','','','','','','','','','<nousers>','','','$userno','<nousers>')") ||
            die "Bad response from $host:\n$dbh::errstr\n";
    #$dbh->do("update $btable set name='<nousers>',number='$userno',main='<nousers>' where main='<nousers>'") ||
    #        die "Bad response from $host:\n$dbh::errstr\n";
    $dbh->disconnect;

   }

   if ($c_entry{"body"} eq $ENTER_MSG) { 
      # Verify password if Nick Is already in database.
      if ($c_entry{"name"} eq $name && 
         ($body eq "<LogCTK>" || 
          $body eq "<lock>") && 
          $c_entry{"passwd"} ne $passwd) {
           #NEW
           #dbmclose(%DB);
           #&ulockchat($LOG_FILE);

           &enterChat;

print <<END;
  <P ALIGN=CENTER>
  <FONT SIZE=5 COLOR=$ALERT_COLOR>Error:  <I>Chat Nick Is In Use Right Now 
  or Invalid Password For Nick.<BR>
  Please Try Another Nick Name.</FONT>
  </P>
END

           exit 0;
      }

      # Send Mail When A Person Enters The Chat Room
      #if ($NOTIFY == 1) {
      #   if ($ENV{'REMOTE_ADDR'} ne "192.168.1.1" && $ENV{'REMOTE_ADDR'} ne "192.168.1.2") {
      #      local($sendmail) = "/usr/lib/sendmail";
      #      open(SENDMAIL, "| $sendmail -t");
   
      #      print SENDMAIL "To: $ADM_MAIL\n"; 
      #      print SENDMAIL "Subject: $c_entry{\"name\"} Entered $MAIN_TITLE\n\n"; 
      #      print SENDMAIL "+++$c_entry{\"name\"}+++"; 
      #      print SENDMAIL "$ENV{'REMOTE_ADDR'}\t"; 
      #      print SENDMAIL "$ENV{'REMOTE_ADDR'}\n\n"; 
      #      print SENDMAIL "$ENV{'HTTP_USER_AGENT'}\n"; 
      #      print SENDMAIL "++++++++++++++++++++++++"; 
      #      close(SENDMAIL);
      #   }
      #}

      $ur = "(";
      $ur .= "'$lmnths[$mon]',";
      $ur .= "'$lmday',";
      $ur .= "'$lhour',";
      $ur .= "'$lmin',";
      $ur .= "'$lsec',";
      $ur .= "'$ENV{'REMOTE_ADDR'}.$c_entry{\"name\"}',";
      $ur .= "'$c_entry{\"size\"}',";
      $ur .= "'$c_entry{\"color\"}',";
      $ur .= "'$c_entry{\"hurl\"}',";
      $ur .= "'$c_entry{\"name\"}',";
      $ur .= "'$c_entry{\"passwd\"}',";
      $ur .= "'<LogCTK>',";
 
      $ur .= "'$userno',";
      $person="$c_entry{\"name\"}";
      $remote="$ENV{'REMOTE_ADDR'}.$person";

      $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
        die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

#print ("insert into $btable values $ur'$person')<br>");
#print ("insert into $btable values $ur'$remote')");

      $dbh->do("delete from $btable where main='$person'") ||
            die "Bad response from $dbhost:\n$dbh::errstr\n";
      $dbh->do("delete from $btable where main='$remote'") ||
            die "Bad response from $dbhost:\n$dbh::errstr\n";

      $dbh->do("insert into $btable values $ur'$person')") ||
            die "Bad response from $dbhost:\n$dbh::errstr\n";
      $dbh->do("insert into $btable values $ur'$remote')") ||
            die "Bad response from $dbhost:\n$dbh::errstr\n";

      $dbh->disconnect;
   }

   $dbs = "('$lmnths[$mon]','$lmday','$lhour','$lmin','$lsec','$ENV{'REMOTE_ADDR'}.$c_entry{\"name\"}',";
   $dbs .= "'$c_entry{\"size\"}','$c_entry{\"color\"}',";
   $dbs .= "'$c_entry{\"hurl\"}','$c_entry{\"name\"}','$c_entry{\"passwd\"}','*','$userno','$userno')";

   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
      die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

   $dbh->do("delete from $btable where main='$userno'") ||
      die "Bad response from $host:\n$dbh::errstr\n";
   $dbh->do("insert into $btable values $dbs") ||
      die "Bad response from $host:\n$dbh::errstr\n";
   $dbh->disconnect;

   #  write to database If Chat "Body" Input is NOT NULL. 
   if ($c_entry{"body"} ne "") {
      &writeChat;
   }

   # Remove Old Users After an Amount Of Time 
   &reloadChat;

   # Print Output.
   &printChat;

   exit 0;
}  

########################################
# enterChat: present entrance to Chat  # 
########################################
sub enterChat 
{
print <<END;

  <HTML>
  <HEAD><TITLE> $MAIN_TITLE </TITLE>
  </HEAD>
  <BODY $BACKGROUND LINK=$LINK VLINK=$VLINK TEXT=$TEXT> 

  <P ALIGN=CENTER VALIGN=CENTER>
  <A HREF="$IMG_URL">
  <IMG SRC="$IMG"
  BORDER=0 ALIGN=TOP WIDTH=168 HEIGHT=70></A><BR>
  <B><FONT SIZE=5>$IMG_URL_TXT</FONT></B><BR>
  <B><FONT SIZE=4>$TITLE</FONT></B>

  <CENTER>

  <FONT SIZE=3 COLOR=$E_TEXT>
  Please choose a Chat Handle and Password
  </FONT>

  <FONT COLOR=$B_TEXT>
  <FORM METHOD="POST" ACTION="$BIN_CGI"></FONT>
  <TABLE BORDER=0 CELLPADDING=3 CELLSPACING=0>
  <TR><TD ALIGN=LEFT>
  <FONT COLOR=$TEXT>
  <B><U>Chat Handle</U>:&nbsp;</B>
  </FONT>
  </TD><TD>

  <INPUT TYPE="text" NAME="name" VALUE="" SIZE="20" MAXLENGTH="20">
  <INPUT TYPE="hidden" SIZE="10" MAXLENGTH="10" NAME="body" VALUE="$ENTER_MSG"> 
  </TD></TR>
  <TR><TD ALIGN=LEFT>
  <B><U>Chat Passwd</U>:</B>
  </TD><TD>

  <INPUT TYPE="password" SIZE="20" MAXLENGTH="20" NAME="passwd" VALUE="">
  </TD></TR>
  <TR><TD ALIGN=LEFT>
  <B>Handle Hue:</B>
  </TD><TD>

  <INPUT TYPE="text" SIZE="20" MAXLENGTH="20" NAME="color" VALUE="$TEXT">
  </TD></TR>

  <TR><TD ALIGN=LEFT>
  <FONT SIZE=2><B>Home Page</B>&nbsp; <I>http://</I>
  </FONT>
  </TD><TD>
  <INPUT TYPE="text" SIZE="20" MAXLENGTH="50" NAME="hurl" VALUE="(OPTIONAL)">
  </TD></TR>

  <TR><TD ALIGN=CENTER COLSPAN=2>
  <B>
  Number Of Lines Displayed: &nbsp;
  </B>
  <FONT COLOR=$B_TEXT><b>
  <SELECT NAME="size"><OPTION>10<OPTION>20
  <OPTION>30<OPTION>50<OPTION>75<OPTION>100</SELECT>
  </B></FONT>
  </TD></TR>

  </TABLE>

  <BR>
  <FONT COLOR=$B_TEXT>
  <B>
  <INPUT TYPE="submit" VALUE="Enter $MAIN_TITLE!!">
  </B>
  </FONT>
  <BR>
  <SMALL>
  <b>Chat Version: $VERSION </b></SMALL>
  </FORM>

  </CENTER>

  </BODY></HTML>

END
}

############################################
# printChat: to List Out The Chat Database #
############################################
sub printChat 
{
print <<END;

  <HTML>
  <HEAD>
  <TITLE>$MAIN_TITLE</TITLE>
  </HEAD>
  <BODY $BACKGROUND LINK="$LINK" VLINK="$VLINK" TEXT="$TEXT">

  <UL><UL><UL>
  <P ALIGN=LEFT>
  <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=3" WIDTH="%100"> 
  <TR><TD ALIGN=LEFT VALIGN=TOP>
  <A HREF="$IMG_URL">
  <IMG SRC="$IMG"
  BORDER=0 ALIGN=TOP WIDTH=168 HEIGHT=70></A><BR>
  <FONT SIZE=2>
  <A HREF="$IMG_URL">$IMG_URL_TXT</A>
  </FONT>
  </TD></TR>
  <TR><TD ALIGN=LEFT VALIGN=TOP BGCOLOR="$TBCOLOR">
  <B><U>
  <FONT SIZE=2 COLOR="$TTTEXT">Current Users In $MAIN_TITLE
  </FONT></U></B>
  <BR>

END

############################
#  Print From the Logging  # 
#       database.          #
############################

$i=0;
$n=1000;

$dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
        die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

$sth=$dbh->prepare("select * from $btable where name='<nousers>'") ||
      die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
$sth->execute() ||
      die "Bad Execute $sth::errstr\n";
while (($row = $sth->fetchrow_arrayref))
{
  $nousers=$row->[12];
}

# Statement Limits No. of Users stored in database yet has other problems.

if ($nousers eq "") {
   $dbh->do("delete from $btable where name='<nousers>'") ||
            die "Bad response from $host:\n$dbh::errstr\n";
   $dbh->do("insert into $btable values ('','','','','','','','','','<nousers>','','','$n','<nousers>')") ||
            die "Bad response from $host:\n$dbh::errstr\n";
   # $dbh->do("update $btable set name='<nousers>',number='$n',main='<nousers>' where main='<nousers>'") ||
   #         die "Bad response from $host:\n$dbh::errstr\n";
}
$dbh->disconnect;

while ($n <= $nousers ) {
   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$n'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";
    while (($row = $sth->fetchrow_arrayref))
    {
      $nmnths=$row->[0];
      $nmday=$row->[1];
      $nhour=$row->[2];
      $nmin=$row->[3];
      $nsec=$row->[4];
      $nurl=$row->[5];
      $nsize=$row->[6];
      $ncolor=$row->[7];
      $nhurl=$row->[8];
      $nname=$row->[9];
      $npasswd=$row->[10];
      $nbody=$row->[11];
      $nuserno=$row->[12];
      $nmain=$row->[13];
    }

    $sth=$dbh->prepare("select * from $btable where main='$nname'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";

    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";

    while (($row = $sth->fetchrow_arrayref))
    {
      $p_mnths=$row->[0];
      $p_mday=$row->[1];
      $p_hour=$row->[2];
      $p_min=$row->[3];
      $p_sec=$row->[4];
      $p_url=$row->[5];
      $p_size=$row->[6];
      $p_color=$row->[7];
      $p_hurl=$row->[8];
      $p_name=$row->[9];
      $p_passwd=$row->[10];
      $p_body=$row->[11];
      $p_userno=$row->[12];
      $p_main=$row->[13];
    }

   $dbh->disconnect;

   
   if ($p_body eq "<LogCTK>") {
   $i++;
   @ident=split( /\./, $p_url );

print <<END;
  <!------BEGIN--$p_name-USER------>
  <FONT SIZE=2 COLOR="$TTEXT">
  <NOBR>&nbsp;&nbsp;  
  $p_name\@$ident[0].$ident[1].$ident[2].$ident[3]</A> &nbsp;&nbsp; <I> 
  (Last Seen &nbsp; $nhour:$nmin:$nsec)
  </I>
END

     if ($p_hurl ne "(OPTIONAL)") {
print <<END;
   &nbsp;&nbsp;Home Page:<A HREF="http://$p_hurl">$p_hurl</A>
END
     }

print <<END;
  </NOBR>
  </FONT>
  <BR>
  <!------END--$p_name-USER-------->
END
   }

   $n = $n + 1000;
}

# Divider of Top of Page and Chat
# GroovyChat-$VERSION Perl Program by Chris Kennedy</FONT>
print <<END;
  <FONT SIZE=1 COLOR="$ALERT_COLOR">
  </TD></TR><TR>
  <TD ALIGN=LEFT VALIGN=CENTER BGCOLOR="$CHATBACK">
  <!------DIVIDER--TOP-CHAT--DIVIDER------->
END

$dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
        die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

$sth=$dbh->prepare("select * from $btable where name='<nochat>'") ||
      die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
$sth->execute() ||
      die "Bad Execute $sth::errstr\n";
while (($row = $sth->fetchrow_arrayref))
{
  $nochat=$row->[12];
}

if ($nousers eq "") {
   $dbh->do("delete from $btable where name='<nochat>'") ||
            die "Bad response from $host:\n$dbh::errstr\n";
   $dbh->do("insert into $btable values ('','','','','','','','','','<nochat>','','','$n','<nochat>')") ||
            die "Bad response from $host:\n$dbh::errstr\n";
    #$dbh->do("update $btable set name='<nochat>',number='$n',main='<nochat>' where main='<nochat>'") ||
    #        die "Bad response from $host:\n$dbh::errstr\n";
}
$dbh->disconnect;
$a = $c_entry{"size"};
if ( $a > 100) {
   $a = 100;
}

# Check in case length of chat is smaller than
# Max records requested
$b = $nochat;
$c = $b - $a;
if ($c < 1) {
   $c = 1;
}

while ($c <= $nochat) {
   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$c'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";
    while (($row = $sth->fetchrow_arrayref))
    {
      $pe_mnths=$row->[0];
      $pe_mday=$row->[1];
      $pe_hour=$row->[2];
      $pe_min=$row->[3];
      $pe_sec=$row->[4];
      $pe_url=$row->[5];
      $pe_size=$row->[6];
      $pe_color=$row->[7];
      $pe_hurl=$row->[8];
      $pe_name=$row->[9];
      $pe_passwd=$row->[10];
      $pe_body=$row->[11];
      $pe_userno=$row->[12];
      $pe_main=$row->[13];
    }
    $dbh->disconnect;


if ($pe_body eq $ENTER_MSG) {
print <<END;

  <!------BEGIN--$pe_name-ENTER------>
  <FONT COLOR=$pe_color SIZE=2><I>
  <B>$pe_name</B>
  <U>$pe_body</U> on ($pe_mnths $pe_mday $pe_hour:$pe_min)
  </I></FONT>
<BR>
  <!------END--$pe_name-ENTER------>

END
}

# Change Colons Back Now and HREF Tags
$pe_body =~ s/COLPPP/:/g;
$pe_body =~ s/AHREFE/A HREF=/g;

   if ($pe_body ne "" && $pe_body ne "<lock>" && 
	$pe_body ne $ENTER_MSG) { 

print <<END;
  <!------BEGIN--$pe_name-CHAT---->
  <SMALL>
  <!--[$pe_hour:$pe_min]--></SMALL>
  <FONT SIZE=4 COLOR=$pe_color><B>$pe_name></B> 
  </FONT><FONT SIZE=3 COLOR=$CHAT_TXT>$pe_body</FONT>
  <BR>
  <!------END--$pe_name-CHAT------>
END

   $lst_post = " $pe_mnths $pe_mday $pe_hour:$pe_min:$pe_sec ";
   $lst_name = "$pe_name";
   }

$c = $c + 1;
}

#########################
#  End of Printing From #  
#     database.         #
#########################

if ($i > 1) {
  $p = "'s";
} else {
    $p = "";
  }

    $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $remote="$ENV{'REMOTE_ADDR'}.$c_entry{\"name\"}";
    $sth=$dbh->prepare("select * from $btable where main='$remote'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";

    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";

    while (($row = $sth->fetchrow_arrayref))
    {
      $amnths=$row->[0];
      $amday=$row->[1];
      $ahour=$row->[2];
      $amin=$row->[3];
      $asec=$row->[4];
      $aurl=$row->[5];
      $asize=$row->[6];
      $acolor=$row->[7];
      $ahurl=$row->[8];
      $aname=$row->[9];
      $apasswd=$row->[10];
      $abody=$row->[11];
      $auserno=$row->[12];
      $amain=$row->[13];
    }
    $dbh->disconnect;


print <<END;
  <!------DIVIDER--BOTTOM-CHAT--DIVIDER------->
  </TD></TR><TR>
  <TD ALIGN=LEFT VALIGN=CENTER BGCOLOR="$TBCOLOR">

  <FONT SIZE=2 COLOR="$TTEXT">
  <NOBR>($i) User$p Present. &nbsp;</NOBR> 
  <NOBR>Last Post: 
  $lst_post

  &nbsp; By &nbsp; $lst_name.
  &nbsp;&nbsp;
  </FONT>
  </NOBR>

  
  <NOBR>
  <FONT SIZE="2" 
  COLOR="$TTEXT">
  You Are Known as <B>$aname</B>
  </FONT>
  </NOBR>

  <NOBR>
  &nbsp;&nbsp;
  &nbsp;&nbsp;
  [
  <FONT SIZE=2 COLOR="$TTEXT">
  <A HREF="$EXIT_URL">
  Exit Chat</A>
  </FONT>
  ]
  </NOBR>


  </TD></TR><TR>
  <TD ALIGN=LEFT VALIGN=CENTER>

  <FORM METHOD="POST" ACTION="$BIN_CGI$PG_POS">
  <INPUT TYPE="hidden" NAME="name" value="$aname">

  <INPUT TYPE="hidden" SIZE="8" MAXLENGTH="8" NAME="color"
  VALUE="$acolor">
  <INPUT TYPE="hidden" SIZE="1" MAXLENGTH="1" 
  NAME="size" VALUE="$asize">

  <TEXTAREA NAME="body" COLS=50 ROWS=3 WRAP=VIRTUAL></TEXTAREA>

  <A NAME=bottom>
  <BR>
  <INPUT TYPE=\"submit\"
  VALUE="Post&nbsp;&#38;&nbsp;Refresh">
  <br>
  <SMALL>
  <b>Chat Version $VERSION </b></SMALL>
  </FORM>
  </P>

  </TD></TR>
  </TABLE>
  </UL></UL></UL>

  </BODY></HTML>

END
}

##########################################
# writeChat: puts chat into database     # 
##########################################
sub writeChat
{
   # Flag for Validity of user access to main chat.
   $flag = 0;
   # Write out to database if Body is not NULL.
   if ($c_entry{"name"} eq $name && 
      $body eq "<LogCTK>" || 
      $c_entry{"body"} eq $ENTER_MSG) 
   { 
      $flag = 1;
   }

   if ($flag != 1) {
      &enterChat;
      exit 0;
   }

$dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
        die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

$sth=$dbh->prepare("select * from $btable where name='<nochat>'") ||
      die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
$sth->execute() ||
      die "Bad Execute $sth::errstr\n";
while (($row = $sth->fetchrow_arrayref))
{
  $nochat=$row->[12];
}

   if ($nochat eq "" ) {
   $dbh->do("insert into $btable values ('','','','','','','','','','<nochat>','','','0','<nochat>')") ||
           die "Bad response from $host:\n$dbh::errstr\n";
   } 
   #if ($nochat eq "" || 
   #   $nochat > $MAX_LOG) 
   #{
   ##$dbh->do("delete from $btable where name='<nochat>'") ||
   ##         die "Bad response from $host:\n$dbh::errstr\n";
   ##$dbh->do("insert into $btable values ('','','','','','','','','','<nochat>','','','0','<nochat>')") ||
   ##        die "Bad response from $host:\n$dbh::errstr\n";
   #$dbh->do("update $btable set name='<nochat>',number='0',main='<nochat>' where main='<nochat>'") ||
   #         die "Bad response from $host:\n$dbh::errstr\n";
   #}

   $nochat = $nochat + 1;
   $dbh->do("delete from $btable where name='<nochat>'") ||
            die "Bad response from $host:\n$dbh::errstr\n";
   $dbh->do("insert into $btable values ('','','','','','','','','','<nochat>','','','$nochat','<nochat>')") ||
            die "Bad response from $host:\n$dbh::errstr\n";
   #$dbh->do("update $btable set name='<nochat>',number='$nochat',main='<nochat>' where main='<nochat>'") ||
   #         die "Bad response from $host:\n$dbh::errstr\n";

   $value = "(";
   $value .= "'$lmnths[$mon]',";
   $value .= "'$lmday',";
   $value .= "'$lhour',";
   $value .= "'$lmin',";
   $value .= "'$lsec',";
   $value .= "'$ENV{'REMOTE_ADDR'}.$c_entry{\"name\"}',";
   $value .= "'$c_entry{\"size\"}',";
   $value .= "'$c_entry{\"color\"}',";
   $value .= "'$c_entry{\"hurl\"}',";
   $value .= "'$c_entry{\"name\"}',";
   $value .= "'$c_entry{\"passwd\"}',";
   $value .= "'$c_entry{\"body\"}',";
   $value .= "'$userno',";
   $value .= "'$nochat')";
   $dbh->do("insert into $btable values $value") ||
            die "Bad response from $host:\n$dbh::errstr\n";
  $dbh->disconnect;
} 

##################################
# Start Of reloadChat Function   # 
##################################
sub reloadChat
{
   $fflag = 1;

   if ($c_entry{"name"} eq $name && 
        $body eq "<lock>" && 
        $passwd ne $c_entry{"passwd"}) {
      $fflag = 0;
   }

   if ($fflag != 1) {
      &enterChat;
      exit 0;
   }

   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) ||
           die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

   $sth=$dbh->prepare("select * from $btable where name='<nousers>'") ||
           die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
   $sth->execute() ||
           die "Bad Execute $sth::errstr\n";
   while (($row = $sth->fetchrow_arrayref))
   {
     $nousers=$row->[12];
   }

   $a = $nousers;
   $b = $NMSTART;
   while ($b <= $a) {
   
   $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$b'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";
    while (($row = $sth->fetchrow_arrayref))
    {
      $cmnths=$row->[0];
      $cmday=$row->[1];
      $chour=$row->[2];
      $cmin=$row->[3];
      $csec=$row->[4];
      $curl=$row->[5];
      $csize=$row->[6];
      $ccolor=$row->[7];
      $churl=$row->[8];
      $cname=$row->[9];
      $cpasswd=$row->[10];
      $cbody=$row->[11];
      $cuserno=$row->[12];
      $cmain=$row->[13];
    }

      if ($cmin+$ERS_INT < $lmin || 
        $chour ne $lhour &&
        $lmin > $cmin-(60-$ERS_INT)) 
      {  
    $dbh=DBI->connect("DBI:mysql:$database:$dbhost", $dbusername, $dbpassword) || 
	die "Can't connect to $database on $dbhost:\n$DBI::errstr\n";

    $sth=$dbh->prepare("select * from $btable where main='$cname'") ||
          die "Bad Prepare from $dbhost:\n$dbh::errstr\n";
    $sth->execute() ||
          die "Bad Execute $sth::errstr\n";
    while (($row = $sth->fetchrow_arrayref))
    {
      $emnths=$row->[0];
      $emday=$row->[1];
      $ehour=$row->[2];
      $emin=$row->[3];
      $esec=$row->[4];
      $eurl=$row->[5];
      $esize=$row->[6];
      $ecolor=$row->[7];
      $ehurl=$row->[8];
      $ename=$row->[9];
      $epasswd=$row->[10];
      $ebody=$row->[11];
      $euserno=$row->[12];
      $emain=$row->[13];
    }

         if ($cname ne $c_entry{"name"}) {
            $dbh->do("delete from $btable where main='$cname'") ||
                 die "Bad response from $dbhost:\n$dbh::errstr\n";
            $dbh->do("insert into $btable values ('$emnths','$emday','$ehour','$emin','$esec','$eurl','$ecolor','$esize','$ehurl','$ename','$epasswd','<lock>','$b','$cname')") ||
                 die "Bad response from $host:\n$dbh::errstr\n";
            $dbh->do("delete from $btable where main='$eurl'") ||
                 die "Bad response from $dbhost:\n$dbh::errstr\n";
         }  
      }
      $b = $b+1000;
   }
}

######################################
# Calculate The Local Time. Function # 
######################################
sub localTime
{
   @lmnths = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
   ($lsec,$lmin,$lhour,$lmday,$mon,$year,$wday,$yday,$isdst) = 
   	localtime(time);
   $lmday = "0$lmday" if ($lmday < 10);
   $lmin = "0$lmin" if ($lmin < 10);
   $lsec = "0$lsec" if ($lsec < 10);
   if ($lhour < 12) {
      $dtflg = "AM";
   }
   else {
      $dtflg = "PM";
   }
   $llhour = ($lhour - 12) if ($lhour > 12);
   $llhour = (12) if ($lhour == 0);
}


###############
# End Of File #
###############
