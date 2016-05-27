%undefine _hardened_build

Name:           moc
Epoch:          1
Version:        2.6
Release:        0.1.alpha2%{?dist}
Summary:        Music on Console - Console audio player for Linux/UNIX
Group:          Applications/Multimedia
License:        GPLv2+ and GPLv3+
URL:            http://moc.daper.net/
Source0:        http://ftp.daper.net/pub/soft/%{name}/unstable/%{name}-%{version}-alpha2.tar.xz

# Fix rpmlint E: incorrect-fsf-address
Patch0:         trivial-update-FSF-address.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  faad2-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  file-devel
BuildRequires:  flac-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libao-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdb-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libmad-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  libogg-devel
BuildRequires:  librcc-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libtimidity-devel
BuildRequires:  libtool
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libvorbis-devel
BuildRequires:  ncurses-devel
BuildRequires:  popt-devel
BuildRequires:  speex-devel
BuildRequires:  taglib-devel
BuildRequires:  wavpack-devel
BuildRequires:  zlib-devel

%description
MOC (music on console) is a console audio player for LINUX/UNIX designed to be
powerful and easy to use. You just need to select a file from some directory
using the menu similar to Midnight Commander, and MOC will start playing all
files in this directory beginning from the chosen file.

%prep
%autosetup -n %{name}-%{version}-alpha2 -p1

%build
%configure \
       --prefix=/usr \
       --without-rcc \
       --with-oss \
       --with-alsa \
       --with-jack \
       --with-aac \
       --with-mp3 \
       --with-musepack \
       --with-vorbis \
       --with-flac \
       --with-wavpack \
       --with-sndfile \
       --with-modplug \
       --with-ffmpeg \
       --with-speex \
       --with-samplerate \
       --with-curl  \
       --disable-cache \
       --disable-debug

%make_build V=1

%install
%make_install

%{__rm} -r %{buildroot}%{_docdir}/%{name}
%{__rm} -r %{buildroot}%{_libdir}/%{name}/decoder_plugins/lib*.la

%files
%doc AUTHORS README* config.example.in keymap.example
%license COPYING
%{_bindir}/%{name}p
%{_datadir}/%{name}
%{_libdir}/%{name}/decoder_plugins/lib*.so
%{_mandir}/man1/%{name}p.1.*

%changelog
* Fri May 27 2016 nrechn <neil@gyz.io> - 2.6-0.1.alpha2
- Update to 2.6-alpha2

* Sun Nov 01 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.6.alpha1
- Hardened builds on <F23

* Tue Sep 29 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.5.alpha1
- Update to svn commit #2776
- Used %%license macro

* Tue Mar 24 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.4.alpha1
- Update to svn commit #2770

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 2.6-0.3.alpha1
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-0.2.alpha1
- Rebuilt for FFmpeg 2.4.x

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.6-0.1.alpha1
- Leap to 2.6-alpha1 release

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-2
- Spec cleanups

* Sat Aug 30 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-1
- Update to release 2.5.0 (Consolidation)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 2.5.0-0.16.beta2
- Rebuilt for ffmpeg-2.3
- Conditional builds for ARM

* Tue May 13 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.15.beta2
- New svn commit of MOC-2.5.0 pre-release (r2641)

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> 2.5.0-0.14.beta2
- Rebuilt for ffmpeg-2.2

* Thu Mar 20 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.13.beta2
- New svn commit of MOC-2.5.0 pre-release
- Fixed release increment number for the pre-releases

* Wed Feb 26 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.12.beta2
- Fix unstripped-binary-or-object warnings for ARM builds

* Wed Feb 05 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.11.beta2
- Update to 2.5.0-beta2
- Removed previous patches

* Tue Jun 18 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.10.beta1
- Added patchset to fix "Unsupported sample size!" error
  See http://moc.daper.net/node/862 for more details
- Added patch for 'sizeof' argument bug
- Added BR: Autoconf and Automake-1.13 (temporarily)
- 'configure.in' renaming

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
