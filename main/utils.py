import numpy as np
import plotly.graph_objects as go

# Geodezik Kubbe Sabitleri
POLYHEDRON_NAMES = {
    3: 'Tetrahedron',
    4: 'Octahedron',
    5: 'Icosahedron',
    6: 'Hexahedron',
    7: 'Heptahedron',
    8: 'Octahedron_8',
    9: 'Enneahedron'
}


# Hesaplama Fonksiyonları
def generate_dome_geometry(params):
    t = int(params.get('type', 5)) # Varsayılan olarak 5 (Icosahedron)
    if t not in range(3, 10):
        raise ValueError('Geçersiz yüz sayısı. 3 ile 9 arasında olmalıdır.')
    
    dome = params.copy()
    dome['poly_name'] = POLYHEDRON_NAMES.get(t, f'Polyhedron_{t}')
    return polyhedron_base(dome, t)

def polyhedron_base(dome, face):
    # Web formundan gelen veriler string olabileceği için sayıya çeviriyoruz
    sp = float(dome['span'])
    ht = float(dome['height'])
    fr = int(dome['freq'])
    
    R = ((sp / 2) ** 2 / ht + ht) / 2
    if ht > R:
        raise ValueError('Kubbe yüksekliği yarıçapı aşamaz.')
        
    alpha = np.degrees(np.arcsin(sp / (2 * R)))
    phi = alpha / fr
    dome['radius'], dome['angle'], dome['fr_angle'] = R, alpha, phi

    ds = sum(range(1, fr + 1)) * face + 1
    dome['nodenum'] = ds
    nodes = np.zeros((ds, 4))

    es = (sum(range(1, fr + 1)) * 3 - fr) * face
    dome['memnum'] = es
    eleman = np.zeros((es, 2), dtype=int)
    mem = np.zeros((es, 5))

    nodes[0] = [1, 0, 0, ht]
    dx = [nodes[0:1]]

    j = 0
    for i in range(1, fr + 1):
        rx = R * np.sin(np.radians(phi * i))
        ar = 2 * np.pi / (face * i)
        aci = np.arange(0, 2 * np.pi, ar)
        ll = np.arange(j + 1, j + 1 + len(aci))

        nodes[ll, 0] = ll + 1
        nodes[ll, 1] = rx * np.cos(aci)
        nodes[ll, 2] = rx * np.sin(aci)
        nodes[ll, 3] = R * np.cos(np.radians(phi * i)) - (R - ht)

        j += len(aci)
        dx.append(nodes[ll])

    dome['nodes'] = nodes

    idx = 0
    top_idx = int(dx[0][0, 0]) - 1
    ring_idx = (dx[1][:, 0] - 1).astype(int)

    for nid in ring_idx:
        eleman[idx] = [nid, top_idx]
        idx += 1

    for i in range(1, fr):
        d2 = (dx[i + 1][::i + 1, 0] - 1).astype(int)
        d1 = (dx[i][::i, 0] - 1).astype(int)
        for a, b in zip(d1, d2):
            eleman[idx] = [a, b]
            idx += 1

    for i in range(1, fr + 1):
        k = (dx[i][:, 0] - 1).astype(int)
        for a, b in zip(k, np.roll(k, -1)):
            eleman[idx] = [a, b]
            idx += 1

    for i in range(1, fr):
        d2 = (dx[i + 1][:, 0] - 1).astype(int)
        d1 = (dx[i][:, 0] - 1).astype(int)
        d2x = (dx[i + 1][::i + 1, 0] - 1).astype(int)
        tmp = np.hstack([np.setdiff1d(d2, d2x)[-1:], np.setdiff1d(d2, d2x)])
        for a, t1, t2 in zip(d1, tmp, np.roll(tmp, -1)):
            eleman[idx] = [a, t1]
            eleman[idx + 1] = [a, t2]
            idx += 2

    mem[:, 0] = np.arange(1, len(eleman) + 1)
    mem[:, 1:3] = eleman + 1
    dome['members'] = mem

    supp = dx[-1].copy()
    supp[:, 1:4] = 1
    dome['support'] = supp.astype(int)

    return dome

def grpdet(dome, tol=1e-6):
    pairs = dome['members'][:, 1:3].astype(int) - 1
    lengths = np.linalg.norm(
        dome['nodes'][pairs[:, 0], 1:4] - dome['nodes'][pairs[:, 1], 1:4],
        axis=1
    )
    groups, unique = {}, []
    for idx, L in enumerate(lengths):
        for gid, UL in enumerate(unique):
            if abs(L - UL) < tol:
                groups.setdefault(gid, []).append(idx)
                break
        else:
            unique.append(L)
            groups[len(unique) - 1] = [idx]
    dome['groups'] = groups
    dome['lengths'] = lengths
    dome['group_count'] = len(groups)
    dome['total_length'] = float(np.sum(lengths))
    return dome

def define_supports(dome):
    dome['supports'] = dome['support'][:, 0].astype(int)
    return dome

# ---------------------------------------------
# Görselleştirme (Plotly) Fonksiyonu
# ---------------------------------------------
def create_dome_plot(dome, group_style='Colored'):
    fig = go.Figure()
    nodes = dome['nodes']
    members = dome['members'][:, 1:3].astype(int)

    if group_style == 'Colored':
        palette = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        for gid, elems in dome['groups'].items():
            color = palette[gid % len(palette)]
            for ei in elems:
                a, b = members[ei] - 1
                p1, p2 = nodes[a, 1:4], nodes[b, 1:4]
                fig.add_trace(go.Scatter3d(
                    x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
                    mode='lines', line=dict(color=color, width=3), showlegend=False
                ))
    else:
        for a, b in members:
            p1, p2 = nodes[a-1, 1:4], nodes[b-1, 1:4]
            fig.add_trace(go.Scatter3d(
                x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
                mode='lines', line=dict(color='lightgray', width=2), showlegend=False
            ))

    # Düğüm noktalarını (Nodes) ekle
    fig.add_trace(go.Scatter3d(
        x=nodes[:, 1], y=nodes[:, 2], z=nodes[:, 3],
        mode='markers', marker=dict(size=3, color='black'), name='Nodes'
    ))

    # Kamera ve Görünüm Ayarları
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600 # Grafiğin HTML'deki varsayılan yüksekliği
    )
    
    return fig