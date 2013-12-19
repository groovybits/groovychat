# Chat.cfg -- Groovy-Chatter CGI Configuration File
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

Go to CPAN at http://www.perl.com/CPAN and get the DBI and DBD Modules

MySQL SQL Server, or most any other standard SQL Server if you have the Linux/NT
libraries for it.  MySQL is available at http://www.mysql.org.

The Database name is CHATROOM and the table used is CHATBASE.  To create the 
Database you can run the dbcreate script, it uses the tools.cfg file to
setup database access paramaters

The Perl Modules DBD DBI and MySQL-Modules are needed, they are on http://www.perl.com/CPAN


mysql> show columns from CHATBASE;
+--------+-----------+------+-----+---------+-------+---------------------------------+
| Field  | Type      | Null | Key | Default | Extra | Privileges                      |
+--------+-----------+------+-----+---------+-------+---------------------------------+
| month  | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| day    | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| hour   | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| min    | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| sec    | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| url    | char(30)  | YES  |     | NULL    |       | select,insert,update,references |
| size   | char(2)   | YES  |     | NULL    |       | select,insert,update,references |
| color  | char(8)   | YES  |     | NULL    |       | select,insert,update,references |
| hurl   | char(30)  | YES  |     | NULL    |       | select,insert,update,references |
| name   | char(25)  | YES  |     | NULL    |       | select,insert,update,references |
| passwd | char(16)  | YES  |     | NULL    |       | select,insert,update,references |
| body   | char(255) | YES  |     | NULL    |       | select,insert,update,references |
| number | char(16)  | YES  |     | NULL    |       | select,insert,update,references |
| main   | char(100) | YES  |     | NULL    |       | select,insert,update,references |
+--------+-----------+------+-----+---------+-------+---------------------------------+

Chris Kennedy 2000
