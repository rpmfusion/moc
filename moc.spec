# Set up a new macro to define MOC's 'mocp' executable
%global     exec   mocp

Name:    moc
Summary: Music on Console - Console audio player for Linux/UNIX
Version: 2.5.0
Release: 0.9.beta1%{?dist}
License: GPLv2+ and GPLv3+
URL:     http://www.moc.daper.net
Source0: http://ftp.daper.net/pub/soft/moc/unstable/%{name}-%{version}-beta1.tar.bz2

## This patch corrects all outdated FSF address
Patch0: %{name}-r2506+fsf_addr.patch

BuildRequires: pkgconfig(ncurses) 
BuildRequires: pkgconfig(alsa) 
BuildRequires: pkgconfig(jack)
BuildRequires: pkgconfig(libcurl) 
BuildRequires: pkgconfig(samplerate) 
BuildRequires: ffmpeg-devel
BuildRequires: pkgconfig(taglib) 
BuildRequires: pkgconfig(speex) 
BuildRequires: libmad-devel 
BuildRequires: pkgconfig(id3tag) 
BuildRequires: pkgconfig(vorbis) 
BuildRequires: pkgconfig(flac) 
BuildRequires: pkgconfig(zlib) 
BuildRequires: pkgconfig(sndfile) 
BuildRequires: pkgconfig(libmodplug) 
BuildRequires: pkgconfig(libtimidity) 
BuildRequires: pkgconfig(wavpack) 
BuildRequires: libdb-devel 
BuildRequires: libtool-ltdl-devel 
BuildRequires: gettext-devel 
BuildRequires: pkgconfig(opus)
BuildRequires: libtool
BuildRequires: librcc-devel

Requires: ffmpeg  
Requires: opus

%description
MOC (music on console) is a console audio player for LINUX/UNIX designed to be
powerful and easy to use. You just need to select a file from some directory
using the menu similar to Midnight Commander, and MOC will start playing all
files in this directory beginning from the chosen file.

%prep
%setup -q -n %{name}-%{version}-beta1
%patch0 -p1 -b %{name}-r2506+fsf_addr.patch

%build
%configure --disable-static --with-rcc \
           --with-oss --with-alsa --with-jack --with-aac --with-mp3 \
           --with-musepack --with-vorbis --with-flac --with-wavpack  \
           --with-sndfile --with-modplug --with-ffmpeg --with-speex  \
           --with-samplerate --with-curl
make %{?_smp_mflags}

%install
%make_install
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -f $RPM_BUILD_ROOT%_libdir/*.la
rm -f $RPM_BUILD_ROOT%_libdir/moc/decoder_plugins/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README README_equalizer AUTHORS ChangeLog COPYING config.example keymap.example NEWS
%dir %{_datadir}/%{name}
%{_bindir}/%{exec}
%{_datadir}/%{name}/themes/*
%{_mandir}/man1/%{exec}.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/decoder_plugins

%changelog
* Sat Jun 08 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.9.beta1
- Removed some explicit Requires (curl, jack-audio-connection-kit, ncurses, speex)

* Fri Jun 07 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.8.beta1
- Fixed Source0 line
- Package owns %%{_libdir}/%%{name} directory

* Mon May 20 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.7.beta1
- Dist tag changed to %%{?dist}

* Tue Apr 09 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.6.beta1
- Removed autoreconf task from %%build section

* Fri Apr 05 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.5.beta1
- Removed libRCC explicit require

* Sun Mar 03 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.4.beta1
- Removed DESTDIR from %%make_install
- Changed source link with a public one
- Set up a new macro to define MOC's 'mocp' executable
- Added %%{name} prefix to the patch

* Tue Dec 25 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.3.beta1
- Added librcc support (fixes encoding in broken mp3 tags)

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.2.beta1
- Added patch to fix FSF address

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.1.beta1
- 2.5.0-beta1
