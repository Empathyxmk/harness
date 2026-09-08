package org.netbeans.modules.php.twig.editor;

import org.junit.Test;
import static org.junit.Assert.*;
import org.openide.filesystems.FileObject;
import org.openide.filesystems.FileSystem;
import org.openide.filesystems.FileUtil;
import org.openide.filesystems.LocalFileSystem;
import org.openide.filesystems.Repository;
import org.openide.loaders.DataObjectExistsException;
import org.openide.loaders.MultiFileLoader;
import org.openide.nodes.Node;
import org.openide.util.Lookup;

import java.io.File;
import java.io.IOException;

public class TwigDataObjectTest {

    private static class DummyFileLoader extends MultiFileLoader {
        public DummyFileLoader() {
            super("org.netbeans.modules.php.twig.editor.TwigDataObject");
        }
        @Override
        protected FileObject findPrimaryFile(FileObject fo) {
            return fo;
        }
        @Override
        protected MultiDataObject createMultiObject(FileObject fo) throws DataObjectExistsException, IOException {
            return null;
        }
    }

    private FileObject createMemoryFileObject() throws IOException {
        java.io.File tmpdir = new File(System.getProperty("java.io.tmpdir"));
        FileObject tempDir = FileUtil.toFileObject(FileUtil.normalizeFile(tmpdir));
        FileObject fo = tempDir.createData("test", "twig");
        return fo;
    }

    @Test
    public void testTwigDataObjectConstruction() throws Exception {
        FileObject fo = createMemoryFileObject();
        MultiFileLoader loader = new DummyFileLoader();
        TwigDataObject obj = new TwigDataObject(fo, loader);
        assertNotNull(obj);
        assertNotNull(obj.getLookup());
    }

    @Test
    public void testCreateNodeDelegateReturnsDataNode() throws Exception {
        FileObject fo = createMemoryFileObject();
        MultiFileLoader loader = new DummyFileLoader();
        TwigDataObject obj = new TwigDataObject(fo, loader);
        Node n = obj.createNodeDelegate();
        assertNotNull(n);
        assertEquals("org.openide.loaders.DataNode", n.getClass().getName());
    }
}