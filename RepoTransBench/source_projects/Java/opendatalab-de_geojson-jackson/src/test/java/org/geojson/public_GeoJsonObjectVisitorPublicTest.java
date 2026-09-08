package org.geojson;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;

import java.util.Arrays;
import java.util.Collection;

@RunWith(Parameterized.class)
public class public_GeoJsonObjectVisitorPublicTest {

	private final GeoJsonObject geoJsonObject;
	private GeoJsonObjectVisitor<GeoJsonObject> instance = new GeoJsonObjectVisitor<GeoJsonObject>() {

		@Override
		public GeoJsonObject visit(GeometryCollection geoJsonObject) {
			Assert.assertEquals(GeometryCollection.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(FeatureCollection geoJsonObject) {
			Assert.assertEquals(FeatureCollection.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(Point geoJsonObject) {
			Assert.assertEquals(Point.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(Feature geoJsonObject) {
			Assert.assertEquals(Feature.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(MultiLineString geoJsonObject) {
			Assert.assertEquals(MultiLineString.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(Polygon geoJsonObject) {
			Assert.assertEquals(Polygon.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(MultiPolygon geoJsonObject) {
			Assert.assertEquals(MultiPolygon.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(MultiPoint geoJsonObject) {
			Assert.assertEquals(MultiPoint.class, geoJsonObject.getClass());
			return geoJsonObject;
		}

		@Override
		public GeoJsonObject visit(LineString geoJsonObject) {
			Assert.assertEquals(LineString.class, geoJsonObject.getClass());
			return geoJsonObject;
		}
	};
	public public_GeoJsonObjectVisitorPublicTest(GeoJsonObject geoJsonObject) {
		this.geoJsonObject = geoJsonObject;
	}

	@Parameterized.Parameters
	public static Collection<Object[]> data() {
		// Use distinct data for public test:
		return Arrays.asList(new Object[][] { 
				{ new GeometryCollection() }, 
				{ new FeatureCollection() },
				{ new Point(-22.55, 145.12345) },
				{ new Feature() }, 
				{ new MultiLineString(Arrays.asList(new LngLatAlt(-23.9, 150.001))) }, 
				{ new Polygon() },
				{ new MultiPolygon() }, 
				{ new MultiPoint() }, 
				{ new LineString() } 
			});
	}

	@Test
	public void should_visit_right_class_public() {
		GeoJsonObject result = geoJsonObject.accept(this.instance);
		Assert.assertEquals(geoJsonObject, result);
	}

	@Test
	public void itShouldAdapter_public() throws Exception {
		Assert.assertNull(geoJsonObject.accept(new GeoJsonObjectVisitor.Adapter<Void>()));
	}
}