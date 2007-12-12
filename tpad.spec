%define name	tpad
%define version	1.3
%define release	%mkrel 2

Name:		%{name}
Summary:	Windows XP (TM) enhanced Notepad clone written in Tcl/Tk
Version:	%{version}
Release:	%{release}
Source0:	http://monitor.deis.unical.it/ant/tpad/%{name}-%{version}.tar.bz2
Patch0:		tpad-1.3.patch.bz2
URL:		http://tclpad.sourceforge.net
Group:		Editors
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
Requires:	tk >= 8.4
Requires:	tcl
BuildArch:	noarch

%description
Apart from all the features Notepad has, tpad adds plugins
to invoke some common text utilities without leaving the
editor, an Ascii table, a tip database and support for
regexps. It also is fully configurable.
 
The executable `tpad' is a wish(1) shell script.

%prep  
%setup -q -c %{name}-%{version}
%patch0 -p1 -b .ant

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%_menudir
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%name
?package(%{name}):command="/usr/bin/tpad" \
icon="editors_section.png" needs="X11" section="More Applications/Editors" \
title="TPad" longtitle="Simple clone of Notepad"
EOF

install -d $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_libdir}/tpad%{version}/msgs
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -d $RPM_BUILD_ROOT/%{_mandir}/man1
install -d $RPM_BUILD_ROOT/%{_datadir}/tpad
install bin/tpad $RPM_BUILD_ROOT/%{_bindir}/tpad
for libfile in lib/tpad%{version}/*.tcl; do
	install $libfile $RPM_BUILD_ROOT/%{_libdir}/tpad%{version};
done
for msgfile in lib/tpad%{version}/msgs/*.msg; do
	install $msgfile $RPM_BUILD_ROOT/%{_libdir}/tpad%{version}/msgs;
done
install etc/tpad.conf $RPM_BUILD_ROOT/%{_sysconfdir}/tpad.conf
install man/man1/tpad.1 $RPM_BUILD_ROOT/%{_mandir}/man1/tpad.1
for datafile in share/tpad/*; do
	install $datafile $RPM_BUILD_ROOT/%{_datadir}/tpad;
done

cd $RPM_BUILD_ROOT/%{_bindir}
ln -sf tpad tview
cd $RPM_BUILD_ROOT/%{_mandir}/man1
ln -sf tpad.1 tview.1

%clean 
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus} 

%postun
%{clean_menus} 

%files
%defattr(-,root,root,0755)
%doc share/doc/tpad/bug.html share/doc/tpad/ChangeLog share/doc/tpad/conf.html share/doc/tpad/embed.html share/doc/tpad/index.html share/doc/tpad/intro.html share/doc/tpad/keys.html share/doc/tpad/log.html share/doc/tpad/mouse.html share/doc/tpad/tidy.html share/doc/tpad/tidy.png share/doc/tpad/todo share/doc/tpad/tpad.html
%{_mandir}/man1/tpad.1*
%{_mandir}/man1/tview.1*
%{_bindir}/tpad
%{_bindir}/tview
%{_libdir}/tpad%{version}
%{_datadir}/tpad
%{_menudir}/%name
%defattr(644,root,root,0755)
%config(noreplace) %{_sysconfdir}/tpad.conf

