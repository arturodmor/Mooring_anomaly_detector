# set ExecFile [file join {C:\Program Files\Compass\Tdyn16.2.5 x64\problemtypes\compassfem.gid\exec} Tdyn.exe]

# catch {exec $ExecFile -name $DataFile$i.flavia -seawaves}


set directorio "D:\arturo_sim\simulaciones\acoplado\prueba"

set archivos [glob -nocomplain -directory $directorio *]

foreach archivo $archivos {
    set ExecFile [file join {C:\Program Files\Compass\Tdyn16.2.5 x64\problemtypes\compassfem.gid\exec} Tdyn.exe]
    set comando "exec $ExecFile -name $archivo -seawaves"
    
    catch {set salida [eval $comando]}
}