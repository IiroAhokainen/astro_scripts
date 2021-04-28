# Script will correct .hoc file from neuromorpho.org.
# In order to make the correction, same data is needed from
# Neuron's import3D tool.
# CNS-GROUP, Tampere University



def fix_commas(IMPORT3D_FILE, _3DVIEWER_FILE):
    """ 
    This will correct commas, change "user7" to "dendrite" 
    and will seek "OrginalDendrite" value. Returns False if
    there was a problem opening the file.
    
    :return orgdend = OrginalDendrite
    """
    k = 0
    a = 0
    orgdend = "Error"
    try:
        with open(IMPORT3D_FILE, 'r+') as i3file:
            lines_i = i3file.readlines()

            with open(_3DVIEWER_FILE, 'r+') as _3dfile:
                lines_view = _3dfile.readlines()
                _3dfile.seek(0)

                for line_v in lines_view:
                    # fix commas
                    if "pt3dadd" in line_v:
                        k += 1
                        for line_i in lines_i:
                            if "pt3dadd" in line_i:
                                a = a + 1
                            if k == a and "]" not in line_i:  # when line is normal
                                line_i = line_i.strip('\t')
                                line_i = "  " + line_i
                                _3dfile.write(line_i)
                                a = 0
                                break
                            elif k == a and "]" in line_i:  # line is unnormal
                                parts = line_i.split('\t')
                                line_i = "  " + parts[1]
                                _3dfile.write(line_i)
                                a = 0
                                break

                    elif "create user7" in line_v:
                        b = line_v.split("[")
                        orgdend = str(b[1]).replace("]", "")
                        orgdend = orgdend.replace("}", "")

                    elif "] connect" in line_v:
                        list_ = line_v.split(" ")

                        if "," in list_[3]:
                            list_[3] = list_[3].replace(",", ".")
                            new_line = " ".join(list_)
                            new_line = new_line.replace("user7", "dendrite")
                            _3dfile.write(new_line)
                        else:
                            line_v = line_v.replace("user7", "dendrite")
                            _3dfile.write(line_v)

                    elif "user7" in line_v:
                        new_line = line_v.replace("user7", "dendrite")
                        _3dfile.write(new_line)

                    else:
                        _3dfile.write(line_v)
                _3dfile.truncate()
        return str(orgdend)

    except:
        print("There was a problem opening import3D file.")
        return False


def delete_curly_braces(_3DVIEWER_FILE):
    """ Deletes unneeded braces. """
    with open(_3DVIEWER_FILE, 'r+') as _3dfile:
        lines_view = _3dfile.readlines()
        _3dfile.seek(0)

        for line_v in lines_view:
            if "create" in line_v or "access" in line_v:
                new_line = line_v.replace("{", "")
                new_line = new_line.replace("}", "")
                _3dfile.write(new_line)
            else:
                _3dfile.write(line_v)
        _3dfile.truncate()


def insert(orgdend, _3DVIEWER_FILE):
    """ Adds needed lines to 3Dviewer code. """
    with open(_3DVIEWER_FILE, 'r+') as _3dfile:
        lines = _3dfile.readlines()

        lines.insert(5, "OriginalDendrite=" + str(orgdend) + "\n")
        lines.insert(6, "NumberDendrites=OriginalDendrite+2*(OriginalDendrite-1)" + "\n")
        lines.insert(7, "SeedNumber=OriginalDendrite-1" + "\n")
        lines.insert(8, "\n")
        lines.insert(10, "create dendrite[NumberDendrites]" + "\n")
        _3dfile.seek(0)
        _3dfile.truncate()
        _3dfile.writelines(lines)
        print("Corrections was made to", _3DVIEWER_FILE, "file.")


def check_file(_3DVIEWER_FILE):
    """ This checks if file has already been fixed with this program. """
    try:
        with open(_3DVIEWER_FILE, 'r') as _3dfile:
            lines = _3dfile.readlines()

            for line in lines:
                if "OriginalDendrite=" in line:
                    print(_3DVIEWER_FILE, "is not orginal file from neuromorpho 3Dviewer.")
                    return False
            return True
    except:
        print("There was a problem opening 3Dviewer file.")
        return False


def main():
    """ Correct file from 3D viewer. """

    IMPORT3D_FILE = input("Import3D file: ")
    _3DVIEWER_FILE = input("3Dviewer file: ")

    if check_file(_3DVIEWER_FILE):
        orgdend = fix_commas(IMPORT3D_FILE, _3DVIEWER_FILE)
        if not orgdend:
            return
        else:
            delete_curly_braces(_3DVIEWER_FILE)
            insert(orgdend, _3DVIEWER_FILE)

main()






