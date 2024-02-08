import ezdxf



if __name__ == "__main__":
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\10._1.dxf')
    msp = doc.modelspace()
    # print(msp.get_redraw_order())
    withoutcapside_insert = msp.query(f'INSERT[name=="VP.221209_withoutcapside"]')[0]
    # msp.set_redraw_order(tuple(list((insert.dxf.handle,insert.dxf.name) for insert in msp.query('INSERT'))))

    for i in msp.query('INSERT'):
        if round(i.dxf.insert[0],2) == round(withoutcapside_insert.dxf.insert[0]):
            i.set_redraw_order(solid.dxf.name, solid.dxf.name)



    for i in msp.get_redraw_order():
        print(i)
    msp.add_blockref(name='nameplate',
                     insert=(100, 0))
    msp.add_blockref(name='DIN_VP.221209',
                     insert=(100,0))


    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\10._1check.dxf')

