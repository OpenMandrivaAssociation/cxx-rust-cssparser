%define libname %mklibname cxx-rust-cssparser
%define develname %mklibname cxx-rust-cssparser -d

Summary:	Library for parsing CSS using the Rust cssparser crate
Name:		cxx-rust-cssparser
Version:	1.1.0
Release:	1
License:	BSD-2-Clause
Group:		System/Libraries
URL:		https://invent.kde.org/libraries/cxx-rust-cssparser
Source0:	https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Corrosion)
BuildRequires:	cargo
BuildRequires:	rust-packaging
BuildRequires:	ninja

BuildSystem:	cmake
BuildOption:	-DBUILD_DOCS:BOOL=OFF
BuildOption:	-DBUILD_TESTING:BOOL=OFF
BuildOption:	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON

%description
C++ bindings around the Rust cssparser crate, used by Union (the Plasma
style engine) to parse CSS-based style descriptions.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
Headers and CMake files for developing applications that use %{name}.

%prep
%autosetup -p1
tar -C rust -xf %{SOURCE1}
mkdir -p rust/.cargo
cat > rust/.cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

# Corrosion's ninja rule runs `cargo install cxxbridge-cmd --locked`.
# Preinstall the lockfile's cxxbridge so cmake find_program() skips that rule.
%conf -p
export CARGO_NET_OFFLINE=true
export CARGO_HOME="$PWD/rust/.cargo"
cargo install cxxbridge-cmd --version 1.0.199 --offline --root "$PWD/_cxxbridge"
export PATH="$PWD/_cxxbridge/bin:$PATH"

%build -p
export CARGO_NET_OFFLINE=true
export CARGO_HOME="$PWD/rust/.cargo"
export PATH="$PWD/_cxxbridge/bin:$PATH"

%files -n %{libname}
%{_libdir}/libcxx-rust-cssparser.so.*

%files -n %{develname}
%{_includedir}/cxx-rust-cssparser
%{_libdir}/libcxx-rust-cssparser.so
%{_libdir}/cmake/cxx-rust-cssparser
%{_bindir}/cxx-rust-cssparser-parse
